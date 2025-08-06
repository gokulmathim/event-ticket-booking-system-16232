from flask.views import MethodView
from flask_smorest import Blueprint, abort
from app.schemas import (
    UserRegisterRequestSchema, UserResponseSchema,
    UserLoginRequestSchema
)
from app import models, auth

blp = Blueprint(
    "Users", "users", url_prefix="/users",
    description="User management endpoints"
)

@blp.route("/register")
class UserRegister(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(UserRegisterRequestSchema)
    @blp.response(201, UserResponseSchema)
    def post(self, user_data):
        """Register a new user."""
        if models.get_user_by_email(user_data["email"]):
            abort(409, message="User already exists.")
        user = models.create_user(
            email=user_data["email"],
            name=user_data["name"],
            password_hash=auth.hash_password(user_data["password"])
        )
        return {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }

@blp.route("/login")
class UserLogin(MethodView):
    # PUBLIC_INTERFACE
    @blp.arguments(UserLoginRequestSchema)
    @blp.response(200, UserResponseSchema)
    def post(self, login_data):
        """Authenticate user and return user details if success."""
        user = models.get_user_by_email(login_data["email"])
        if not user or not auth.verify_password(login_data["password"], user["password_hash"]):
            abort(401, message="Invalid credentials")
        return {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        }
