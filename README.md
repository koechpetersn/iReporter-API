# iReporter-API
[![Build Status](https://travis-ci.org/koechpetersn/iReporter-API.svg?branch=ch-test-endpoints-162337791)](https://travis-ci.org/koechpetersn/iReporter-API)

<a href="https://codeclimate.com/github/koechpetersn/iReporter-API/maintainability"><img src="https://api.codeclimate.com/v1/badges/8ad00b39780d187adb28/maintainability" /></a>


[![Coverage Status](https://coveralls.io/repos/github/koechpetersn/iReporter-API/badge.svg?branch=develop)](https://coveralls.io/github/koechpetersn/iReporter-API?branch=develop)




A backend for a web application that helps users to create incident records and manipulate their them.

### Branches
* develop - all the features developed.
* features - contains all the features created.
* chores - contains tests and lfa feedback implementation


### Prerequisites
What you need to get started:
    
    Python 3: https://www.python.org/downloads/
    Flask: http://flask.pocoo.org/docs/1.0/installation/
    Flask_restful: https://flask-restful.readthedocs.io/en/latest/installation.html
    Pytest: https://docs.pytest.org/en/latest/getting-started.html
    


## Running and testing app
# Running:
```
$ virtualenv venv
$ cd venv
$ git clone https://github.com/koechpetersn/iReporter-API
$ source venv/bin/activate
$ cd iReporter-API
$ export APP_SETTINGS=development
$ python run.py
```

# Testing

Follow the steps above then:

$ pytest

## Endpoints

| URL                    | METHODS   | DESCRIPTION                    |
| :---                   |     :---: |          ---:                  |  
| `/api/v1/incidents`    | POST      | Admin Create an incident       |
| `/api/v1/incidents`    | GET       | Fetch all incidents            |
| `/api/v1/incidents/1`  | GET       | Fetch a single incident        | 
| `/api/v1/incidents/1`  | PATCH     | Admin edit an incident record  |
| `/api/v1/incidents/1`  | DELETE    | Admin delete  an incident      |



# Hosting 
https://ireporter-koech.herokuapp.com/api/v1/incidents


# Author

Peter Koech

# Contributions

This repo can be forked and contributed to.

[![Build Status](https://travis-ci.org/koechpetersn/iReporter-API.svg?branch=ch-test-endpoints-162337791)](https://travis-ci.org/koechpetersn/iReporter-API)[![Coverage Status](https://coveralls.io/repos/github/koechpetersn/iReporter-API/badge.svg)]((https://coveralls.io/github/koechpetersn/iReporter-API)
