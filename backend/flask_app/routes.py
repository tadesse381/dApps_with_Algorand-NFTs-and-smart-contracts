"""Routes for parent Flask app."""
from flask import request, jsonify
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    unset_jwt_cookies,
    jwt_required
)
import json
from datetime import datetime, timezone, timedelta


def init_routes(app, User):
    """A factory function that takes in the server 
    object and initializes the routes.
    """
    @app.route("/test")
    def test():
        return "Hello, world"

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            print(get_jwt())
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                data = response.get_json()
                if type(data) is dict:
                    data["access_token"] = access_token
                    response.data = json.dumps(data)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original respone
            return response

    @app.route('/signup', methods=["POST"])
    def signup():
        email = request.json.get("email", None)
        password = request.json.get("password", None)
        first_name = request.json.get("first_name", None)
        last_name = request.json.get("last_name", None)

        user = User(
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        user.password = password
        user.save()
        

        
        return {"msg": "account created successfully"}, 201

    @app.route('/login', methods=["POST"])
    def login():
        email = request.json.get("email", None)
        password = request.json.get("password", None)

        user = User.objects(email=email).first()
        print(f"User found: {user.to_json()}")
        if not user.verify_password(password):
            return {"msg": "Wrong email or password"}, 401

        access_token = create_access_token(identity=email)
        response = {"access_token": access_token}
        return response

    @app.route("/logout", methods=["POST"])
    def logout():
        response = jsonify({"msg": "logout successful"})
        unset_jwt_cookies(response)
        return response

    @app.route('/user')
    @jwt_required()
    def user_info():
        response_body = {
            "name": "user-name",
            "msg": "Hello! you have successfully used the jwt token"
        }

        return response_body

    return app
