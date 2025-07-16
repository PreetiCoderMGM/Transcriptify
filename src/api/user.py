from flask import Blueprint
from flask import request, jsonify

from src.api.response_utils import send_response
from src.bl.action_result import ActionResult, ResultCode
from src.db.sql.user import User
from src import db
from src.utils import get_uid
from logger_util import get_logger

log = get_logger(__name__)
user_blueprint = Blueprint("user_blueprint", __name__)


@user_blueprint.route("/user/sign_up", methods=['POST'])
def sign_up():
    req_id: str = get_uid()
    try:
        data = request.get_json()
        email = data.get('email')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        if not email:
            return jsonify({"success": False, "message": "Email is required.", "request_id": req_id}), 400
        # Check if user already exists
        existing_user = User.get_by_email(email)
        if existing_user:
            return jsonify({"success": False, "message": "User with this email already exists.",
                            "request_id": req_id}), 409
        # Create new user
        new_user = User(email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        db.session.commit()
        result: ActionResult = ActionResult(ResultCode.Ok, message="User registered successfully.", req_id=req_id,
                                            http_res_status=200)
        return send_response(result)
    except Exception as ex:
        log.exception(f"Request failed. Reason: Exception: {ex}, request_id: {req_id}.")
        return jsonify({"success": False, "message": "Internal server error.", "request_id": req_id}), 500
