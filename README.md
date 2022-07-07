# testing_reqres
A short test using python with https://reqres.in/


## Installation
Developed using Python 3.8.6. I recommend to use pyenv.

`pip install -r requirements.txt`

## Execute
In the project root, run

`pytest -q tests/test_users_endpoint.py -s`

## Pytest
Pytest allow us to use `check` functions, that won't stop tests on failures but still faile the execution if checks fails. Creating a report of fails founded.
It also allow us to still use `assert` if we need to ensure a condition and stop the test if it fail.
https://docs.pytest.org/en/7.1.x/