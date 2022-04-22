# About

This project was developed based on [Origin Backend Take Home Assignment](https://github.com/OriginFinancial/origin-backend-take-home-assignment).

Here I have developed an HTTP Rest API in Python, Flask Framework as a web server and Flask Restx (it is a Flask extension to make Rest API development faster).

I am more experienced developing Rest APIs in Java with SpringBoot, but I decided to learn how to do develop them with Python since it was a preference for this project. Working with SpringBoot also made me search for a framework to speed up things, so that is why I used Flask for this one.

To make the code cleaner and extensible I decided to separate the code in two main classes where the first one - RiskProfile - is handling the API routes and the second one - RiskProfileService - is handling the business rules.
In the file insurance_risk_calculator.py, that contains the class RiskProfile, I also defined a model/schema for the API input, allowing to make the code more readable and extensible.



## How to run

To get this project running, you must have installed:
- Python 3 (I have developed and tested using the version 3.8.2)
- Flask (pip install flask)
- Flask Restx (pip install flask-restx)

Then, in the source folder (src), run the application by typing the command into your command line:
``python3 app.py``

This will start the application within the Flask server in the localhost and port 5000.

## How to consume the API