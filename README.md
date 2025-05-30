# Restful Booker API Testing Project

## Project Overview

This project demonstrates a comprehensive approach to API testing using the Restful Booker public API, which simulates a hotel booking management system. The goal is to showcase skills in designing, automating, and validating REST API endpoints to ensure functional correctness, robustness, and basic performance.

## Tools and Technologies

- **API Tested:** https://restful-booker.herokuapp.com  
- **Programming Language:** Python 3.12  
- **Test Framework:** Pytest  
- **HTTP Client:** Requests  
- **Continuous Integration:** GitHub Actions (to be configured)  
- **Development Environment:** Visual Studio Code, Git

## Project Structure

    restful_booker_api_tests/
    ├── tests/
    │ └── test_booking_api.py # Automated API tests
    ├── .github/
    │ └── workflows/
    │ └── api-tests-ci.yml # CI/CD workflow configuration
    ├── requirements.txt # Python dependencies
    └── README.md # Project documentation

## Setup Instructions

1. **Clone the repository** or download the project files.  
2. **Install dependencies** with pip:

```bash
pip install -r requirements.txt

run
```bash
pytest tests/

Tests cover authentication, CRUD operations for bookings, error handling, negative test cases (marked as expected failures), and basic performance.

Notes
Negative tests are marked with xfail because the Restful Booker API is permissive and accepts malformed data without error.

This project demonstrates professional handling of such API limitations by documenting expected failures.