# API Test Report – Restful Booker

## 1. Project Context

This project demonstrates my QA skills through testing the realistic public RESTful API **Restful Booker**, which simulates a hotel booking management platform.

The main objective is to design, execute, and automate a comprehensive suite of functional and negative tests to ensure the quality and robustness of key endpoints such as authentication, booking CRUD operations, error handling, and performance.

## 2. Environment and Tools Used

- **API Tested:** https://restful-booker.herokuapp.com  
- **Language:** Python 3.12  
- **Test Framework:** Pytest  
- **HTTP Library:** Requests  
- **CI/CD Pipeline:** To be integrated later with GitHub Actions  
- **Development Tools:** VSCode, Git

## 3. Test Coverage

| Category                  | Description                                                          | Number of Tests |
|---------------------------|----------------------------------------------------------------------|-----------------|
| Authentication            | Validation of token success and authentication failure               | 2               |
| Booking Creation          | Valid creation, missing fields, invalid formats                      | 5 (including 3 marked as expected failures) |
| Booking Retrieval         | Valid retrieval, non-existent booking retrieval                      | 2               |
| Booking Update            | Update with and without valid token                                  | 2               |
| Booking Deletion          | Deletion with and without valid token                                | 2               |
| List Bookings             | Retrieval of the complete bookings list                              | 1               |
| Advanced Negative Testing | Invalid data, JSON injection attempts, malformed formats (expected failures) | 3               |
| Performance Testing       | Response time below 0.5 seconds                                      | 1               |

## 4. Summary of Results

- All functional tests for authentication and CRUD operations passed successfully, confirming the API's functional compliance.
- Advanced negative tests have been implemented but are marked as expected failures (`xfail`) because the Restful Booker API is permissive and does not enforce strict server-side validation.
- Basic performance test confirms response times under 0.5 seconds on booking list retrieval.

## 5. Identified Limitations

The tested API is designed for demonstration purposes and does not fully replicate strict validation behavior expected in production environments. As a result:

- Malformed or suspicious data inputs are frequently accepted without error.
- In real-world scenarios, backend robustness against invalid data should be verified, which this API does not fully simulate.

This limitation is explicitly addressed by marking the relevant tests as expected failures, demonstrating professional handling of technical constraints and appropriate adaptation of testing strategy.

## 6. Conclusion

This project highlights my ability to:

- Build a comprehensive and automated test suite for a REST API.
- Handle both positive and negative test scenarios professionally.
- Document technical limitations and adjust testing approaches accordingly.
- Implement basic performance indicators.

This methodology is directly transferable to freelance projects to ensure API quality and robustness, while facilitating effective communication with development teams.
