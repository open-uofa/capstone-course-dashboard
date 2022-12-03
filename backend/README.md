# Backend Documentation

## Contents

[Usage](#usage)
1. [Dependencies](#dependencies)
2. [Database Connection](#database-connection)
3. [Google Connection](#google-connection)
4. [GitHub Connection](#github-connection)
5. [Running the Backend](#running-the-backend)
6. [Documentation](#documentation)

[Development](#development)
1. [Structure](#structure)
2. [Code Style](#code-style)
3. [Unit Testing](#unit-testing)
4. [Integration Testing](#integration-testing)
5. [Setting up GitHub Actions](#setting-up-github-actions)


# Usage

Instructions for running the backend.


## Dependencies

Please install the required Python dependencies using `pip install -r backend/requirements.txt`
within the `backend` directory.


## Database Connection

To connect to a database, first create a `.env` file in the `backend/app/server` directory,
or add to it if it already exists. Follow the template here:
```
MONGODB_ADDRESS=<DATABASE_IP>
DB_NAME=<DATABASE_NAME>
```

This requires an IPv6 internet connection if connecting to a remotely hosted database on Cybera.


## Google Connection

The backend uses Google OAuth for authentication. A client ID needs to be created on the Google
Cloud Platform for the backend to connect to. Follow
[these instructions](https://support.google.com/cloud/answer/6158849?hl=en) to set it up.

Once it has been set up, add the following origins on the Cloud Console. Note that the
`localhost` and `127.0.0.1` origins are not necessary if the frontend is hosted on a domain:
```
Authorized JavaScript origins
http://localhost:5173
http://localhost
http://127.0.0.1
http://127.0.0.1:5173
http://<Frontend URL (ex. Cybera domain URL)>
https://<Frontend URL (ex. Cybera domain URL)>

Authorized redirect URIs
http://localhost:5173
http://localhost
http://127.0.0.1
http://127.0.0.1:5173
http://<Frontend URL (ex. Cybera domain URL)>
https://<Frontend URL (ex. Cybera domain URL)>
```

Now we need to generate a secret key for the backend to use for token authentication.
Run the following command in a Python interpreter:
```
$ python3
import secrets
generated_key = secrets.token_urlsafe(30)
print(generated_key)
```
Add the generated key to the `.env` file created above:
```
API_SECRET_KEY=<YOUR_GENERATED_KEY>
```

Now authentication will be checked against Google OAuth. Note that the actual sign-in is
performed on the frontend.


## GitHub Connection

### Overview

There are four ways to do GitHub API authentication. The first is basic authentication, which
is unsafe and thus not considered. Another way is to use personal access tokens, however,
this is mainly meant for one-time uses. The other two ways are using an OAuth App or a GitHub App.
The GitHub App does everything that the OAuth App can do, with even more features, and
is GitHub's recommended way to do authentication. This is what we are currently using.


For GitHub Apps, there are a few methods of using them for authentication.


We can either do it through a web interface (client side) or we can do it server side.
The client side method requires a client ID and secret.
The server side method requires a private key and app ID.
Since we want to process the data we get from GitHub, we will need to get the token to the
back-end eventually. Thus, it makes more sense to perform the authentication solely through
the back-end.

### Setup

First, a GitHub App needs to be created. This can either be for a user or for an organization.
Follow [these steps](https://docs.github.com/en/developers/apps/building-github-apps/creating-a-github-app)
to set up the App. Here, the permissions for the app can be set. Ensure that Content is set to
read-only. Also, ensure this App is private so that it can only be added to your account.


Once the App is created, GitHub gives you a private key for it (download this). Additionally,
there will be a corresponding App ID. These two things will be important for our project.
There is also the option to limit the app to specific repositories. Feel free to set these
to the desired repositories.


Add a few variables to the `.env` file created above:
```
GITHUB_APP_ID=<YOUR_APP_ID>
GITHUB_PRIVATE_KEY_PATH=<PATH/TO/PRIVATE/KEY.pem>
```


Now the backend will be able to connect to your GitHub account and fetch data for the available
repositories.


### Meeting Minutes

The backend will automatically fetch meeting minutes from the repositories it has access to.
These are scraped from the team's MKDocs, which are expected to be hosted on GitHub Pages
at the following URL: `https://{owner}.github.io/{team}/meeting_minutes/`

The format of the meeting minutes in MKDocs is expected to be as follows:
```
# === "Title for tab, must be some sort of date"
# Meeting minutes content (can be anything))

# === "Another title"
# More meeting minutes content
```


## Running the backend

To run the backend, from the `backend/app` directory, use the following command: `python main.py`

It will be available at http://localhost:8000.

For reference, here is the full `.env` file:
```
MONGODB_ADDRESS=<DATABASE_IP>
DB_NAME=<DATABASE_NAME>
GITHUB_APP_ID=<YOUR_APP_ID>
GITHUB_PRIVATE_KEY_PATH=<PATH/TO/PRIVATE/KEY.pem>
API_SECRET_KEY=<YOUR_SECRET_KEY>
```


## Documentation

Documentation can be found at http://localhost:8000/docs. Due to our authentication setup,
these docs are view only, as there is no way to authenticate without using the frontend to log in
with Google OAuth.


# Development

Guidelines for modifying the backend.


## Structure

The backend uses [FastAPI](https://fastapi.tiangolo.com) to implement REST API endpoints.
The high level directory structure is as follows:
```
backend/ (Backend root directory)
└── app/ (Contains all application code)
    ├── server/ (The actual API code)
    │   ├── models/ (Request and response models)
    │   ├── routes/ (API endpoint functions)
    │   ├── util/ (Utility functions called by the API endpoints)
    │   ├── app.py (Combines all the endpoint routers into a single app)
    │   └── config.py (Loads environment variables)
    ├── tests/ (Contains all tests)
    │   ├── integration/ (Integration tests)
    |   |   ├── config.py (Loads environment variables and contains test data)
    |   |   └── conftest.py (Fixtures for integration tests)
    │   └── unit/ (Unit tests)
    |       ├── conftest.py (Fixtures for unit tests)
    |       └── mock_data.py (Mock data that all unit tests can access)
    └── main.py (Runs the app using uvicorn)
```


## Code Style

We enforce strict Python style guides for the backend following Python's [PEP 8](https://pep8.org).

To run formatting and style checks, a script has been provided in the `backend/app` directory.

First change the script to be executable: `chmod +x style.sh`

Then run it using: `./style.sh`
This will fix any formatting and import order issues, and will also run a linter to check for
any other style issues. These issues will be printed to the console and need to be fixed manually.

For more specific formatting commands:

The backend uses [isort](https://pycqa.github.io/isort/) to manage import order.
To fix all imports, run the following within the `backend/app` directory:
```
isort --profile black server/ tests/
```

The backend uses [black](https://black.readthedocs.io/en/stable/) to manage code formatting.
To automatically format, run the following within the `backend/app` directory:
```
black server/ tests/
```
Note: VS Code also supports the option to use black to format on save.

The backend uses [pylint](https://pylint.pycqa.org/en/latest/index.html) to manage Python code style.
To check for errors, run the following within the `backend/app` directory:
```
# For the main API files.
pylint server/
# For the testing files.
pylint tests/
```
Pylint errors can sometimes be false positive, so in the case that you are sure that your code
is correct, you can add a `# pylint: disable=<error>` comment to the line that is causing the
error. If pylint complains about something that is required for a lot of code to work
(ex. test fixtures), you can disable the rule globally in the `.pylintrc` file.
We have a separate `.pylintrc` file for the tests, as we have a different set of rules for them.
See `backend/app/.pylintrc` and `backend/app/tests/.pylintrc` for more details.


## Unit Testing

The goal of unit testing is to test each function individually without needing to rely on any
specific environment setup. Currently we add unit tests for all helper functions and for all
API functions.
We are using [pytest](https://docs.pytest.org) combined with
[pytest-mock](https://pytest-mock.readthedocs.io) (based on unittest.mock) for testing.

To run tests: `pytest app/tests/unit`

This assumes it is being run from the `backend` directory. Modify the path if running the command
elsewhere. You can also specify the specific file to run, or even the specific test to run.

Ex. `pytest app/tests/unit/test_auth_routes::test_submit_auth`

### Writing unit tests with pytest

#### Fixtures

`conftest.py` contains functions called
[fixtures](https://docs.pytest.org/en/7.1.x/how-to/fixtures.html) that can be used anywhere within
the `tests/unit` directory. These fixtures are simply passed as parameters to the test function
that needs them. The main point of fixtures is to take care of setup and cleanup operations to
prepare the environment for the test being run. Fixtures can return values using the `yield`
statement - anything before the yield is run before the test is run, and anything after the yield
runs after the test is run. Note that you can change the scope of the fixture so that it doesn't
only encapsulate a single test, instead it can persist for the whole class scope, or even the whole
testing session.


There are two major utility fixtures currently added:
- `response_mock`: Mocks Python requests' Response object so that we can modify the data returned
in the response. There isn't really a simple way to do that in one line.
- `mock_settings`: Sets all our environment variables to mock values. This way we do not need to
rely on a .env file being present.

#### Mocking

To mock external function calls like requests, database queries, etc., we can use pytest-mock's
mocker fixture. Simply include it as a function parameter and use it like so at the start of the test:
```
mocker.patch("target.to.patch", return_value="optional", etc.)
```
Now when you call the function you're testing, all calls to the patched function will be mocked.
There is a special case for patching Python requests' methods. Set the return_value to be a
`response_mock` object instead of the raw data you want to return:
```
def test_something(mocker, response_mock):
    mocker.patch("requests.get", return_value=response_mock({"value": "test"}))
```

To save on code duplication, we can store mock test data in the `/tests/unit/mock_data.py` file.
This is mainly helpful for larger objects so that our test files don't get too long.

#### Assertions

In pytest, we can either use the `assert` keyword to check that one value equals another value,
or we can use pytest-mock's assertions, which are used like so:
```
m = mocker.patch(...)
m.assert_called_once()
m.assert_called_once_with(...)
# etc.
```
See
[here](https://docs.python.org/3/library/unittest.mock.html?highlight=assert_called#the-mock-class)
for further documentation.


## Integration Testing

The goal of integration testing is to test each API endpoint with all external connections.
Just like unit tests, we are using pytest, and most of the testing strategies will remain the same
(aside from mocking).

To run tests: `pytest app/tests/integration`

### Environment

The integration tests should run as-is, as long as the .env file has been set up for the main
FastAPI app. However, there is the option to customize some of the environment variables by
creating a new .env file in the `tests/integration` directory. Here is a sample template:
```
MONGODB_ADDRESS=<DATABASE_IP>
DB_NAME=<DATABASE_NAME>
GITHUB_APP_ID=<YOUR_APP_ID>
GITHUB_PRIVATE_KEY_PATH=<PATH/TO/PRIVATE/KEY.pem>
GITHUB_OWNER=<OWNER_OF_GITHUB_APP>
GITHUB_REPO=<GITHUB_REPOSITORY_TO_FETCH_DATA_FROM>
```

### Writing integration tests with pytest

#### Fixtures

There are four major utility fixtures currently added:
- `set_test_db`: This overrides the app's environment files if any new values have been provided
for the testing environment.
- `client`: This is the most important fixture to use in tests. The client object will allow you
to make calls to the API endpoints as if you are accessing them through an HTTP call.
- `clean_database`: This cleans the environment before we start running tests. The test database
will be wiped and a new one will be created with our template data. By default, this will use a
database called `test_db`.
- `token`: This is a JWT token that can be used to make authenticated calls to the API. It is
needed for any tests that require authentication.


## Setting up GitHub Actions

All backend formatting checks and testing can be run automatically using GitHub Actions.
To use a self hosted runner, follow [these steps](https://docs.github.com/en/actions/hosting-your-own-runners/adding-self-hosted-runners).

To run integration tests on the self-hosted instance, create a folder called `env` in the
root directory. This folder should contain the following files:
- `.env` (The `.env` file for the main FastAPI app. We recommend using a specific database only for testing)
- `pk.pem` (private key for GitHub app)
