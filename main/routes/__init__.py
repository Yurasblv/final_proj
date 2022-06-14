from flask_restx import Api

from .profile.routes import apireg, apilogin, apilogout
from .service.routes import apifilms, apimethods

api = Api(title="MyAPI", version="1.0", description="My simple RESTAPI")

api.add_namespace(apireg)
api.add_namespace(apilogin)
api.add_namespace(apilogout)
api.add_namespace(apifilms)
api.add_namespace(apimethods)
