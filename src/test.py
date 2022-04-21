import unittest
from unittest.mock import patch
from service.risk_profile_service import RiskProfileService

from datetime import date

class TestRiskProfile(unittest.TestCase):

    def test_when_user_has_no_income(self):
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
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 0,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_eligibility_by_ownership(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["eligible"], 0)

    def test_when_user_has_no_vehicles(self):
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
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 200000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": None
        }

        RiskProfileService.calculate_eligibility_by_ownership(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["auto"]["eligible"], 0)

    def test_when_user_has_no_houses(self):
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
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": None,
            "income": 200000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_eligibility_by_ownership(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["home"]["eligible"], 0)

    def test_when_user_age_is_above_60(self):
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
        risk_profile = {
            "age": 61,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 200,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_eligibility_by_age(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["eligible"], 0)
        self.assertEqual(insurance["life"]["eligible"], 0)
        self.assertEqual(insurance["home"]["eligible"], 1)
        self.assertEqual(insurance["auto"]["eligible"], 1)

    def test_when_user_age_is_29(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 29,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 200,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_risk_by_age(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 1)
        self.assertEqual(insurance["life"]["risk_score"], -1)
        self.assertEqual(insurance["home"]["risk_score"], -2)
        self.assertEqual(insurance["auto"]["risk_score"], 0)

    def test_when_user_age_is_35(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 200,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_risk_by_age(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 2)
        self.assertEqual(insurance["life"]["risk_score"], 0)
        self.assertEqual(insurance["home"]["risk_score"], -1)
        self.assertEqual(insurance["auto"]["risk_score"], 1)

    def test_when_user_income_is_greater_than_200k(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "owned"},
            "income": 201000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_risk_by_income(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 2)
        self.assertEqual(insurance["life"]["risk_score"], 0)
        self.assertEqual(insurance["home"]["risk_score"], -1)
        self.assertEqual(insurance["auto"]["risk_score"], 1)

    def test_when_user_house_is_mortgaged(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 201000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_risk_by_house(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 4)
        self.assertEqual(insurance["life"]["risk_score"], 1)
        self.assertEqual(insurance["home"]["risk_score"], 1)
        self.assertEqual(insurance["auto"]["risk_score"], 2)

    def test_when_user_has_dependents(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 201000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_risk_by_dependents(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 4)
        self.assertEqual(insurance["life"]["risk_score"], 2)
        self.assertEqual(insurance["home"]["risk_score"], 0)
        self.assertEqual(insurance["auto"]["risk_score"], 2)

    def test_when_user_is_married(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 201000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": 2018}
        }

        RiskProfileService.calculate_risk_by_marital_status(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 2)
        self.assertEqual(insurance["life"]["risk_score"], 2)
        self.assertEqual(insurance["home"]["risk_score"], 0)
        self.assertEqual(insurance["auto"]["risk_score"], 2)

    def test_when_user_vehicle_is_new(self):
        insurance = {
            "life": {
                "eligible": 1,
                "risk_score": 1
            },
            "disability": {
                "eligible": 1,
                "risk_score": 3
            },
            "home": {
                "eligible": 1,
                "risk_score": 0
            },
            "auto": {
                "eligible": 1,
                "risk_score": 2
            }
        }
        risk_profile = {
            "age": 35,
            "dependents": 2,
            "house": {"ownership_status": "mortgaged"},
            "income": 201000,
            "marital_status": "married",
            "risk_questions": [0, 1, 0],
            "vehicle": {"year": date.today().year - 3}
        }

        RiskProfileService.calculate_risk_by_vehicle_age(RiskProfileService, risk_profile, insurance)
        self.assertEqual(insurance["disability"]["risk_score"], 3)
        self.assertEqual(insurance["life"]["risk_score"], 1)
        self.assertEqual(insurance["home"]["risk_score"], 0)
        self.assertEqual(insurance["auto"]["risk_score"], 3)

    @patch('service.risk_profile_service.RiskProfileService.map_score', return_value="ineligible")
    def test_calculate_when_risk_score_is_ineligible(self, mock_map_score):

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
                "eligible": 0,
                "risk_score": 0
            }
        }

        risk_profile_output = {
            "auto": "",
            "disability": "",
            "home": "",
            "life": ""
        }
        
        RiskProfileService.calculate_risk_score(RiskProfileService, insurance, risk_profile_output)
        self.assertEquals(risk_profile_output["auto"], "ineligible")

    def test_when_risk_score_is_ineligible(self):

        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 0, 3), "ineligible")

    def test_when_risk_score_is_below_equals_0(self):

        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 1, -1), "economic")
        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 1, 0), "economic")

    def test_when_risk_score_is_1_or_2(self):

        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 1, 1), "regular")
        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 1, 2), "regular")

    def test_when_risk_score_is_above_equals_3(self):

        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 1, 3), "responsible")
        self.assertEquals(RiskProfileService.map_score(RiskProfileService, 1, 5), "responsible")
    

if __name__ == '__main__':
    unittest.main()

    