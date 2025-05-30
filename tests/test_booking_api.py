import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="session")
def auth_token():
    response = requests.post(f"{BASE_URL}/auth", json={
        "username": "admin",
        "password": "password123"
    })
    assert response.status_code == 200
    return response.json()["token"]

@pytest.fixture
def create_booking(auth_token):
    # Création d'une réservation valide
    payload = {
        "firstname": "John",
        "lastname": "Doe",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-01",
            "checkout": "2025-06-10"
        },
        "additionalneeds": "Breakfast"
    }
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    assert response.status_code == 200
    booking_id = response.json()["bookingid"]
    yield booking_id
    # Cleanup : suppression après test avec le token
    headers = {"Cookie": f"token={auth_token}"}
    requests.delete(f"{BASE_URL}/booking/{booking_id}", headers=headers)

def test_authentication_success():
    response = requests.post(f"{BASE_URL}/auth", json={
        "username": "admin",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "token" in response.json()

def test_authentication_failure():
    response = requests.post(f"{BASE_URL}/auth", json={
        "username": "admin",
        "password": "wrongpassword"
    })
    assert response.status_code == 200
    assert response.json() == {"reason": "Bad credentials"}

def test_create_booking_success(create_booking):
    assert create_booking is not None

def test_create_booking_missing_fields():
    payload = {
        "firstname": "John",
        # lastname manquant volontairement
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-01",
            "checkout": "2025-06-10"
        }
    }
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    # L'API renvoie 500 erreur sur ce payload mal formé
    assert response.status_code == 500

def test_get_booking(create_booking):
    booking_id = create_booking
    response = requests.get(f"{BASE_URL}/booking/{booking_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == "John"

def test_get_nonexistent_booking():
    response = requests.get(f"{BASE_URL}/booking/9999999")
    assert response.status_code == 404

def test_update_booking_success(auth_token, create_booking):
    booking_id = create_booking
    headers = {"Cookie": f"token={auth_token}"}
    payload = {
        "firstname": "Jane",
        "lastname": "Doe",
        "totalprice": 200,
        "depositpaid": False,
        "bookingdates": {
            "checkin": "2025-07-01",
            "checkout": "2025-07-10"
        },
        "additionalneeds": "Lunch"
    }
    response = requests.put(f"{BASE_URL}/booking/{booking_id}", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["firstname"] == "Jane"

def test_update_booking_unauthorized(create_booking):
    booking_id = create_booking
    payload = {
        "firstname": "Hacker",
        "lastname": "NoAuth"
    }
    response = requests.put(f"{BASE_URL}/booking/{booking_id}", json=payload)
    assert response.status_code in (403, 401)

def test_delete_booking_success(auth_token, create_booking):
    booking_id = create_booking
    headers = {"Cookie": f"token={auth_token}"}
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}", headers=headers)
    assert response.status_code in (201, 200)
    # Vérifier la suppression effective
    response_check = requests.get(f"{BASE_URL}/booking/{booking_id}")
    assert response_check.status_code == 404

def test_delete_booking_unauthorized(create_booking):
    booking_id = create_booking
    response = requests.delete(f"{BASE_URL}/booking/{booking_id}")
    assert response.status_code in (403, 401)

def test_list_bookings():
    response = requests.get(f"{BASE_URL}/booking")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.xfail(reason="API très permissive, accepte données invalides sans erreur")
def test_create_booking_invalid_date_format():
    payload = {
        "firstname": "Invalid",
        "lastname": "DateFormat",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "01-06-2025",  # Mauvais format
            "checkout": "10-06-2025"
        },
        "additionalneeds": "None"
    }
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    assert response.status_code == 200

@pytest.mark.xfail(reason="API très permissive, accepte données invalides sans erreur")
def test_create_booking_string_instead_of_bool():
    payload = {
        "firstname": "StringBool",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": "true",  # Devrait être bool
        "bookingdates": {
            "checkin": "2025-06-01",
            "checkout": "2025-06-10"
        }
    }
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    assert response.status_code == 200

@pytest.mark.xfail(reason="API très permissive, accepte données invalides sans erreur")
def test_injection_json_in_fields():
    payload = {
        "firstname": '{"$ne": ""}',  # Tentative d'injection JSON
        "lastname": "Injection",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2025-06-01",
            "checkout": "2025-06-10"
        }
    }
    response = requests.post(f"{BASE_URL}/booking", json=payload)
    assert response.status_code == 200

def test_response_time_under_half_second():
    response = requests.get(f"{BASE_URL}/booking")
    assert response.elapsed.total_seconds() < 0.5
