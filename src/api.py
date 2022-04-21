from flask import Flask
from flask_restx import Resource, Api, fields
from datetime import date

app = Flask(__name__)
api = Api(app)

house = api.model(
    "House",
    {
        "ownership_status": fields.String(required=True, description="Ownership Status")
    }
)

vehicle = api.model(
    "Vehicle",
    {
        "year": fields.String(required=True, description="Vehicle's Year")
    }
)

risk_profile = api.model(
    "RiskProfile",
    {
        "age": fields.Integer(required=True, description="Age"),
        "dependents": fields.Integer(required=True, description="Dependents"),
        "income": fields.Integer(required=True, description="Income"),
        "marital_status": fields.String(required=True, description="Marital Status"),
        "house": fields.Nested(house, required=False, description="House"),
        "vehicle": fields.Nested(vehicle, allow_null=True, required=False, description="Vehicle Info"),
        "risk_questions": fields.List(fields.Integer, required=True, description="Risk Questions")
    }
)

class RiskProfileDAO(object):

    insurance = {
        "life": {
            "eligible": 1,
            "risk_score": 0
        },
        "disability": {
            "eligible": 1,
            "risk_score": 0
        },
        "home": {
            "eligible": 1,
            "risk_score": 0
        },
        "auto": {
            "eligible": 1,
            "risk_score": 0
        }
    }

    risk_profile_output = {
        "auto": "ineligible",
        "disability": "ineligible",
        "home": "ineligible",
        "life": "ineligible"
    }

    def init_insurance(self, insurance):
        insurance["life"]["eligible"] = 1
        insurance["life"]["risk_score"] = 0
        insurance["home"]["eligible"] = 1
        insurance["home"]["risk_score"] = 0
        insurance["disability"]["eligible"] = 1
        insurance["disability"]["risk_score"] = 0
        insurance["auto"]["eligible"] = 1
        insurance["auto"]["risk_score"] = 0

    def init_risk_profile_output(self, risk_profile_output):
        risk_profile_output["auto"] = "ineligible"
        risk_profile_output["disability"] = "ineligible"
        risk_profile_output["home"] = "ineligible"
        risk_profile_output["life"] = "ineligible"
    
    def __init__(self):
        self.counter = 0

    def get_base_score(self, risk_profile):
        base_score = 0
        for question in risk_profile["risk_questions"]:
            print(question)
            base_score += question
        return base_score

    def set_risk_score(self, base_score, insurance):
        insurance["disability"]["risk_score"] = base_score
        insurance["auto"]["risk_score"] = base_score
        insurance["home"]["risk_score"] = base_score
        insurance["life"]["risk_score"] = base_score

    def calculate_eligibility_by_ownership(self, risk_profile, insurance):
        if (risk_profile["income"] == 0):
            insurance["disability"]["eligible"] = 0
        if (risk_profile["vehicle"] is None):
            insurance["auto"]["eligible"] = 0
        if (risk_profile["house"] is None):
            print(risk_profile["house"])
            insurance["home"]["eligible"] = 0

    def calculate_eligibility_by_age(self, risk_profile, insurance):
        if(risk_profile["age"] > 60):
            print(risk_profile["age"])
            insurance["disability"]["eligible"] = 0
            insurance["life"]["eligible"] = 0

    def calculate_risk_by_age(self, risk_profile, insurance):
        if(risk_profile["age"] < 30):
            insurance["disability"]["risk_score"] -= 2
            insurance["auto"]["risk_score"] -= 2
            insurance["home"]["risk_score"] -= 2
            insurance["life"]["risk_score"] -= 2
        if(risk_profile["age"] >= 30 and risk_profile["age"] <= 40):
            insurance["disability"]["risk_score"] -= 1
            insurance["auto"]["risk_score"] -= 1
            insurance["home"]["risk_score"] -= 1
            insurance["life"]["risk_score"] -= 1

    def calculate_risk_by_income(self, risk_profile, insurance):
        if(risk_profile["income"] > 200000):
            insurance["disability"]["risk_score"] -= 1
            insurance["auto"]["risk_score"] -= 1
            insurance["home"]["risk_score"] -= 1
            insurance["life"]["risk_score"] -= 1

    def calculate_risk_by_house(self, risk_profile, insurance):
        if(risk_profile["house"] is not None and risk_profile["house"]["ownership_status"] == "mortgaged"):
            insurance["disability"]["risk_score"] += 1
            insurance["home"]["risk_score"] += 1
    
    def calculate_risk_by_dependents(self, risk_profile, insurance):
        if(risk_profile["dependents"] > 0):
            insurance["disability"]["risk_score"] += 1
            insurance["life"]["risk_score"] += 1

    def calculate_risk_by_marital_status(self, risk_profile, insurance):
        if(risk_profile["marital_status"] == "married"):
            insurance["disability"]["risk_score"] -= 1
            insurance["life"]["risk_score"] += 1

    def calculate_risk_by_vehicle_age(self, risk_profile, insurance):
        if(risk_profile["vehicle"] is not None and risk_profile["vehicle"]["year"] > (date.today().year - 5)):
            insurance["auto"]["risk_score"] += 1

    def map_score(self, eligibility, risk_score):
        if(eligibility == 0):
            return "ineligible"
        elif(risk_score <= 0):
            return "economic"
        elif(risk_score >= 1 and risk_score <= 2):
            return "regular"
        elif(risk_score >= 3):
            return "responsible"

    def calculate_risk_score(self, insurance, risk_profile):
        risk_profile["auto"] = self.map_score(insurance["auto"]["eligible"], insurance["auto"]["risk_score"])
        risk_profile["disability"] = self.map_score(insurance["disability"]["eligible"], insurance["disability"]["risk_score"])
        risk_profile["home"] = self.map_score(insurance["home"]["eligible"], insurance["home"]["risk_score"])
        risk_profile["life"] = self.map_score(insurance["life"]["eligible"], insurance["life"]["risk_score"])
        

    def calculate_risk_profile(self, data):
        risk_profile_input = data
        base_score = self.get_base_score(risk_profile_input)
        print("Base score calculated =", base_score)
        self.init_insurance(self.insurance)
        self.set_risk_score(base_score, self.insurance)
        self.calculate_eligibility_by_ownership(risk_profile_input, self.insurance)
        self.calculate_eligibility_by_age(risk_profile_input, self.insurance)
        self.calculate_risk_by_age(risk_profile_input, self.insurance)
        self.calculate_risk_by_income(risk_profile_input, self.insurance)
        self.calculate_risk_by_house(risk_profile_input, self.insurance)
        self.calculate_risk_by_dependents(risk_profile_input, self.insurance)
        self.calculate_risk_by_marital_status(risk_profile_input, self.insurance)
        self.calculate_risk_by_vehicle_age(risk_profile_input, self.insurance)
        self.init_risk_profile_output(self.risk_profile_output)
        self.calculate_risk_score(self.insurance, self.risk_profile_output)
        print(self.risk_profile_output["auto"])
        print(self.risk_profile_output["disability"])
        print(self.risk_profile_output["home"])
        print(self.risk_profile_output["life"])
        return self.risk_profile_output



#If the user doesn’t have income, vehicles or houses, she is ineligible for disability, auto, and home insurance, respectively.
#If the user is over 60 years old, she is ineligible for disability and life insurance.
#If the user is under 30 years old, deduct 2 risk points from all lines of insurance. If she is between 30 and 40 years old, deduct 1.
#If her income is above $200k, deduct 1 risk point from all lines of insurance.
#If the user's house is mortgaged, add 1 risk point to her home score and add 1 risk point to her disability score.
#If the user has dependents, add 1 risk point to both the disability and life scores.
#If the user is married, add 1 risk point to the life score and remove 1 risk point from disability.
#If the user's vehicle was produced in the last 5 years, add 1 risk point to that vehicle’s score.


DAO = RiskProfileDAO()

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/calculate_risk_profile')
class RiskProfile(Resource):
    def get(self):
        return {'hello': 'world'}

    def post(self):
        return DAO.calculate_risk_profile(api.payload), 200

if __name__ == '__main__':
    app.run(debug=True)