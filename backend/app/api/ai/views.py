from flask import Blueprint, request
from app.api.ai import fetch_bot_response

ai_blueprint = Blueprint("ai_blueprint", __name__)


@ai_blueprint.route("/ai", methods=["POST"])
def chat():
    req = request.get_json()
    question = req.get("question")
    response = fetch_bot_response(question)
    return {"answer": response, "message": "OK"}, 200
