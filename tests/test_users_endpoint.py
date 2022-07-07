import datetime
import pytest_check as check
from backend_services.reqres_backend import ReqResBackend

validationTestExpectedResponseBody = {
            "page": 2,
            "per_page": 6,
            "total": 12,
            "total_pages": 2,
            "data": [
                {
                    "id": 7,
                    "email": "michael.lawson@reqres.in",
                    "first_name": "Michael",
                    "last_name": "Lawson",
                    "avatar": "https://reqres.in/img/faces/7-image.jpg"
                },
                {
                    "id": 8,
                    "email": "lindsay.ferguson@reqres.in",
                    "first_name": "Lindsay",
                    "last_name": "Ferguson",
                    "avatar": "https://reqres.in/img/faces/8-image.jpg"
                },
                {
                    "id": 9,
                    "email": "tobias.funke@reqres.in",
                    "first_name": "Tobias",
                    "last_name": "Funke",
                    "avatar": "https://reqres.in/img/faces/9-image.jpg"
                },
                {
                    "id": 10,
                    "email": "byron.fields@reqres.in",
                    "first_name": "Byron",
                    "last_name": "Fields",
                    "avatar": "https://reqres.in/img/faces/10-image.jpg"
                },
                {
                    "id": 11,
                    "email": "george.edwards@reqres.in",
                    "first_name": "George",
                    "last_name": "Edwards",
                    "avatar": "https://reqres.in/img/faces/11-image.jpg"
                },
                {
                    "id": 12,
                    "email": "rachel.howell@reqres.in",
                    "first_name": "Rachel",
                    "last_name": "Howell",
                    "avatar": "https://reqres.in/img/faces/12-image.jpg"
                }
            ],
            "support": {
                "url": "https://reqres.in/#support-heading",
                "text": "To keep ReqRes free, contributions towards server costs are appreciated!"
            }
        }

expectedUsersNoIDs = [
        {
            "email": "michael.lawson@reqres.in",
            "first_name": "Michael",
            "last_name": "Lawson",
            "avatar": "https://reqres.in/img/faces/7-image.jpg"
        },
        {
            "email": "lindsay.ferguson@reqres.in",
            "first_name": "Lindsay",
            "last_name": "Ferguson",
            "avatar": "https://reqres.in/img/faces/8-image.jpg"
        },
        {
            "email": "tobias.funke@reqres.in",
            "first_name": "Tobias",
            "last_name": "Funke",
            "avatar": "https://reqres.in/img/faces/9-image.jpg"
        },
        {
            "email": "byron.fields@reqres.in",
            "first_name": "Byron",
            "last_name": "Fields",
            "avatar": "https://reqres.in/img/faces/10-image.jpg"
        },
        {
            "email": "george.edwards@reqres.in",
            "first_name": "George",
            "last_name": "Edwards",
            "avatar": "https://reqres.in/img/faces/11-image.jpg"
        },
        {
            "email": "rachel.howell@reqres.in",
            "first_name": "Rachel",
            "last_name": "Howell",
            "avatar": "https://reqres.in/img/faces/12-image.jpg"
        }
    ]

expectedUser11 ={
    "email": "george.edwards@reqres.in",
    "first_name": "George",
    "last_name": "Edwards",
    "avatar": "https://reqres.in/img/faces/11-image.jpg"
}

def validateDateFormat(dateText, dateFormat='%Y-%m-%dT%H:%M:%S.%f%z'):
        try:
            datetime.datetime.strptime(dateText, dateFormat)
        except ValueError:
            return False
        return True

def test_listUsersPage2():
    backend = ReqResBackend()
    responseData = backend.users(ReqResBackend.GET, page=2)
    responseParsedData = responseData["parsedResponse"]
    responseFullData = responseData["response"]

    # Response data validation
    expectedStatusCode = 200
    check.equal(responseFullData.status_code, expectedStatusCode,
                f"Expected statud code f{expectedStatusCode}, found {responseFullData.status_code}")


    # Response content validation
    ### Do some validation testing
    # In cases like this one, could be useful validate the whole document at once.
    check.equal(responseParsedData, validationTestExpectedResponseBody, "Failed validation response body")

    ### If the strategy is validate specific fields we can use this approach
    # First we need to ensure the json schema is valid. W can use existent libraries but keep this simple
    expectedFields = ["page", "per_page", "total", "total_pages", "data", "support"]
    for expectedField in expectedFields:
        # If the field is not found test will fail and stop at this point
        assert(responseParsedData.get(expectedField) is not None), f"Field {expectedField} not found on response body"
    assert(len(list(responseParsedData.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(responseParsedData.keys()))}"

    check.equal(responseParsedData["page"], 2, f"Expected page must be 2, found {responseParsedData['page']}")
    resultsPerPage = responseParsedData["per_page"]
    totalResults = responseParsedData["total"]
    totalPages = responseParsedData["total_pages"]
    # If we know the expected values for these parameters we can check them, one check as example
    expectedResultsPerPage = 6
    check.equal(resultsPerPage, expectedResultsPerPage,
                f"Expected results per page must be {expectedResultsPerPage}, found {resultsPerPage}")


    # If we don't know the expected values but still want to check if the results page distribution is correct
    # based on data we got from the response body
    expectedResultsPerPage = totalResults // totalPages # In this case the division is exact, so i won't complicate thinks calculating pages with smaller size
    check.equal(resultsPerPage, expectedResultsPerPage,
                f"Expected results per page must be {expectedResultsPerPage}, found {resultsPerPage}")

    # In both cases, we need to ensure the amount of data retreived is the expected one
    check.equal(len(responseParsedData["data"]), expectedResultsPerPage,
                f"Expected users must be {expectedResultsPerPage}, found {len(responseParsedData['data'])}")

    # Whe should validate the users content like we did before
    currentUsers = responseParsedData["data"]
    for user in currentUsers:
        # Find the user with ID 11, but i won't use it on this test, because isolation
        if user["id"] == 11:
            OBJECTIVE_USER_ID_11 = user
        #
        expectedFields = ["id", "email", "first_name", "last_name", "avatar"]
        for expectedField in expectedFields:
            # If the field is not found test will fail and stop at this point
            assert(user.get(expectedField) is not None), f"User data - Field {expectedField} not found on user content data"

        # We should validate the user content. We need to know the expected values to do that
        userFound = False
        for expectedUser in expectedUsersNoIDs:
            # Assuming that email will be unique
            if expectedUser["email"] == user["email"]:
                userFound = True
                # Validating just one field as example, but need to do the same with the others fields
                check.equal(expectedUser["first_name"], user["first_name"],
                            f"Expected user fiest_name {expectedUser['first_name']}, found {user['first_name']}")
                break
        check.is_true(userFound, f"User {user['email']} not found on expected users")

    # And finally left to check the support section content, but is similar to previous checks, so i will ignore it

def test_singleUser():
    backend = ReqResBackend()
    responseData = backend.users(ReqResBackend.GET, userID=11)
    responseParsedData = responseData["parsedResponse"]
    responseFullData = responseData["response"]

    # Response data validation
    expectedStatusCode = 200
    check.equal(responseFullData.status_code, expectedStatusCode,
                f"Expected statud code f{expectedStatusCode}, found {responseFullData.status_code}")

    # First we need to ensure the json schema is valid. W can use existent libraries but keep this simple
    expectedFields = ["data", "support"]
    for expectedField in expectedFields:
        # If the field is not found test will fail and stop at this point
        assert(responseParsedData.get(expectedField) is not None), f"Field {expectedField} not found on response body"
    assert(len(list(responseParsedData.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(responseParsedData.keys()))}"

    currentUser = responseParsedData["data"]
    expectedUser = expectedUser11 # We can reuse the retrieved user11 from previous test. But to keep the test isolation we shouldn't

    # Retrieved user fields validation
    expectedFields = ["id", "email", "first_name", "last_name", "avatar"]
    for expectedField in expectedFields:
        # If the field is not found test will fail and stop at this point
        assert(currentUser.get(expectedField) is not None), f"Field {expectedField} not found on response body"
        if expectedField != "id": # excluding ID field because is not in the expected values
            check.equal(currentUser[expectedField], expectedUser[expectedField],
                    f"User field {expectedField} expected value f{expectedUser[expectedField]}, found {currentUser[expectedField]}")

    assert(len(list(currentUser.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(currentUser.keys()))}"

    # And finally left to check the support section content, but is similar to previous checks, so i will ignore it

def test_newUser():
    backend = ReqResBackend()
    expectedUserData = {
        "name": "Peter",
        "job": "Sales"
    }
    responseData = backend.users(ReqResBackend.POST, payload=expectedUserData)
    responseParsedData = responseData["parsedResponse"]
    responseFullData = responseData["response"]

    # Response data validation
    expectedStatusCode = 201
    check.equal(responseFullData.status_code, expectedStatusCode,
                f"Expected statud code f{expectedStatusCode}, found {responseFullData.status_code}")

     # First we need to ensure the json schema is valid. We can use existent libraries but keep this simple
    expectedFields = ["name", "job", "id", "createdAt"]
    for expectedField in expectedFields:
        # If the field is not found test will fail and stop at this point
        assert(responseParsedData.get(expectedField) is not None), f"Field {expectedField} not found on response body"
    assert(len(list(responseParsedData.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(responseParsedData.keys()))}"

    # Ensure the response content
    check.equal(responseParsedData["name"], expectedUserData["name"],
                f"Expected new user name in response f{expectedUserData['name']}, found {responseParsedData['name']}")
    check.equal(responseParsedData["job"], expectedUserData["job"],
                f"Expected new user job in response f{expectedUserData['job']}, found {responseParsedData['job']}")
    # To test the created date we need to know the timezone of the server and compare the value with a current date of the request calculated on the server who run the testsd. 
    # I will skipe it because I miss some of this information.
    # Instead, i will check that the date format is correct
    check.is_true(validateDateFormat(responseParsedData["createdAt"]), f"Date format should be in ISO format, {responseParsedData['createdAt']}")

    # As last step we should check that the user was properly created after this request, retrieving the created user by ID (similar to previous test)
    # Because this time we don't need to check the get request it self, we only need to check if the user is there
    """
    # Commented becasue mock server, prevent test failures
    responseData = backend.users(ReqResBackend.GET, userID=responseParsedData["id"])
    responseParsedData = responseData["parsedResponse"]

    check.equal(responseData["data"]["name"], expectedUserData["name"],
                    f"Created user name expected value f{expectedUserData['name']}, found {responseData['data']['name']}")
    check.equal(responseData["data"]["job"], expectedUserData["job"],
                    f"Created user job expected value f{expectedUserData['job']}, found {responseData['data']['job']}")
    check.equal(responseData["data"]["createdAt"], responseParsedData["createdAt"],
                    f"Created user createdAt expected value f{responseParsedData['createdAt']}, found {responseData['data']['createdAt']}")
    """

def test_registerUnsuccesful():
    backend = ReqResBackend()
    payload = {
        "email": "sydney@fife"
    }
    responseData = backend.register(ReqResBackend.POST, payload=payload)
    responseParsedData = responseData["parsedResponse"]
    responseFullData = responseData["response"]

    # Response data validation
    expectedStatusCode = 400
    check.equal(responseFullData.status_code, expectedStatusCode,
                f"Expected statud code f{expectedStatusCode}, found {responseFullData.status_code}")

    expectedFields = ["error"]
    for expectedField in expectedFields:
        # If the field is not found test will fail and stop at this point
        assert(responseParsedData.get(expectedField) is not None), f"Field {expectedField} not found on response body"
    assert(len(list(responseParsedData.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(responseParsedData.keys()))}"

    expectedErrorMessage = "Missing password"
    check.equal(responseParsedData["error"], expectedErrorMessage,
                f"Expected error message 'f{expectedErrorMessage}', found {responseParsedData['error']}")

    # We should also test the cases:
    #   * email but no password
    #   * no email and no password
    #   * following the error message i found that username could be used instead email, so this is another case 
    # But i will add only the case of missing email, but password is into make it simplier

    payload = {
        "password": "TESTPASSWORD"
    }
    responseData = backend.register(ReqResBackend.POST, payload=payload)
    responseParsedData = responseData["parsedResponse"]
    responseFullData = responseData["response"]

    # Response data validation
    expectedStatusCode = 400
    check.equal(responseFullData.status_code, expectedStatusCode,
                f"Expected statud code f{expectedStatusCode}, found {responseFullData.status_code}")

    expectedFields = ["error"]
    for expectedField in expectedFields:
        # If the field is not found test will fail and stop at this point
        assert(responseParsedData.get(expectedField) is not None), f"Field {expectedField} not found on response body"
    assert(len(list(responseParsedData.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(responseParsedData.keys()))}"

    expectedErrorMessage = "Missing email or username"
    check.equal(responseParsedData["error"], expectedErrorMessage,
                f"Expected error message 'f{expectedErrorMessage}', found {responseParsedData['error']}")

def test_optionaTest():
    backend = ReqResBackend()
    responseData = backend.users(ReqResBackend.GET, page=2)
    responseParsedData = responseData["parsedResponse"]

    expectedUser11 = None
    currentUsers = responseParsedData["data"]
    for user in currentUsers:
        if user["id"] == 11:
            expectedUser11 = user

    responseData = backend.users(ReqResBackend.GET, userID=11)
    responseParsedData = responseData["parsedResponse"]

    currentUser11 = responseParsedData["data"]

    expectedFields = list(expectedUser11.keys())
    for expectedField in expectedFields:
        assert(currentUser11.get(expectedField) is not None), f"Field {expectedField} not found on recovered user"
        check.equal(currentUser11[expectedField], expectedUser11[expectedField],
                    f"User field {expectedField} expected value f{expectedUser11[expectedField]}, found {currentUser11[expectedField]}")
    assert(len(list(currentUser11.keys())) == len(expectedFields)), f"Expected parameters {len(expectedFields)}, but found f{len(list(currentUser11.keys()))}"