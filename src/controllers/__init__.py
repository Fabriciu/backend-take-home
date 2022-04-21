from flask_restx import Api

from .insurance_risk_calculator import api as insurance_api

api = Api(title="Insurance API", version="1.0", description="Insurance API - Origin Backend Take Home",)

api.add_namespace(insurance_api)