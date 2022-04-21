from datetime import date

class RiskProfileService(object):

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

    def get_base_score(self, risk_profile):
        base_score = 0
        for question in risk_profile["risk_questions"]:
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
            insurance["home"]["eligible"] = 0

    def calculate_eligibility_by_age(self, risk_profile, insurance):
        if(risk_profile["age"] > 60):
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
        return self.risk_profile_output

