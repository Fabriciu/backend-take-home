from flask_restx import Resource, Namespace, Api, fields
from datetime import date
from service.risk_profile_service import RiskProfileService

api = Namespace("insurance/v1", description="Insurance API")

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

Service = RiskProfileService()

@api.route('/calculate_risk_profile')
class RiskProfile(Resource):

    def post(self):
        return Service.calculate_risk_profile(api.payload), 200


