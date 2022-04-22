# About

Hello,

I am Fabrício Borgatto. I am a backend developer that has worked in several Rest API projects. You may get more info about me on [Linkedin](https://www.linkedin.com/in/fabricioborgatto/).

This project was developed based on [Origin Backend Take Home Assignment](https://github.com/OriginFinancial/origin-backend-take-home-assignment).

Here I have developed an HTTP Rest API in Python, Flask Framework as a web server and Flask Restx (it is a Flask extension to make Rest API development faster).

I am more experienced developing Rest APIs in Java with SpringBoot, but since Python was a preference for this project and I like learning new things, I decided to learn how to do develop them with Python. I have worked in a few Python scripts before.
Working with SpringBoot also made me search for a framework to speed up things, so that is why I used Flask for this one.

For the API route, I decided to define it as POST method and the resource as /calculate_risk_profile. It is a pattern I have been using when exposing an operation like a calculation engine.

To make the code cleaner and extensible I decided to separate the code in two main classes where the first one - RiskProfile - is handling the API routes and the second one - RiskProfileService - is handling the business rules.

In the file controllers/insurance_risk_calculator.py, that contains the class RiskProfile, I also defined a model/schema for the API input, allowing to make the code more readable and extensible.

In the class RiskProfileService, as a Clean Code principle I decided to write one function for each business rules, so each function does only one thing. That will allow the code maintanability.

The file test.py contains the unittests. I wrote one for each function of RiskProfileService.

The application is missing a logging system, so that is a improvement for a next release. The HTTP error and code exceptions are also improvements to be made to the application.

## How to run

To get this project running, you must have installed:
- Python 3 (I have developed and tested using the version 3.8.2)
- Flask (pip3 install flask)
- Flask Restx (pip3 install flask-restx)

Then, in the source folder (src), run the application by typing the command into your command line:
    ``python3 app.py``


    src fabricioborgatto$: python3 app.py 
    * Serving Flask app 'app' (lazy loading)
    * Environment: production
    WARNING: This is a development server. Do not use it in a production deployment.
    Use a production WSGI server instead.
    * Debug mode: on
    * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
    * Restarting with stat
    * Debugger is active!
    * Debugger PIN: 263-840-006


This will start the application within the Flask server in the localhost and port 5000.

To run the tests, just run the command ``python3 test.py``

    src fabricioborgatto$ python3 test.py
    test.py:415: DeprecationWarning: Please use assertEqual instead.
    self.assertEquals(risk_profile_output["auto"], "ineligible")
    ................
    ----------------------------------------------------------------------
    Ran 16 tests in 0.004s

    OK


## How to call the API

Here is a code snippet for a HTTP Request


    POST /insurance/v1/calculate_risk_profile HTTP/1.1
    Host: 127.0.0.1:5000
    Content-Type: application/json
    Content-Length: 182

    {
        "age": 35,
        "dependents": 2,
        "house": {"ownership_status": "owned"},
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }

In case of any attribute without value, pass a null value to it. For example, when a person does not have a house:

    {
        "age": 35,
        "dependents": 2,
        "house": null,
        "income": 0,
        "marital_status": "married",
        "risk_questions": [0, 1, 0],
        "vehicle": {"year": 2018}
    }
