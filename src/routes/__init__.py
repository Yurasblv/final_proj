from flask_restx import Api
from src.routes.user.routes import apiuser, apilogout, apiregister
from src.routes.film.routes import apifilms, apimethods

api = Api(title="MyAPI", version="1.0", description="My simple RESTAPI")

api.add_namespace(apiregister)
api.add_namespace(apiuser)
api.add_namespace(apilogout)
api.add_namespace(apifilms)
api.add_namespace(apimethods)
