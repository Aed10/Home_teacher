from flask import Blueprint, request, jsonify
from openai import OpenAI
from app.models import Progress, db

client = OpenAI()

main = Blueprint("main", __name__)

# OpenAI API Key (You will need your own key)


@main.route("/api/explain", methods=["POST"])
def explain():
    data = request.json
    problem = data.get("problem", "")

    if not problem:
        return jsonify({"error": "No problem provided"}), 400

    # Call OpenAI GPT for the explanation
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful teacher who is explaining to a student how to solve the following problem:",
                },
                {"role": "user", "content": problem},
            ],
        )
        explanation = response.choices[0].message.content
        return jsonify({"explanation": explanation}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@main.route("/api/revision", methods=["GET"])
def get_revision_plan():
    # Placeholder for now - can be dynamically generated based on user performance
    revision_plan = {
        "topics": ["Algebra", "Trigonometry", "Calculus"],
        "problem_sets": [
            {"topic": "Algebra", "difficulty": "medium"},
            {"topic": "Trigonometry", "difficulty": "hard"},
        ],
    }
    return jsonify(revision_plan), 200


@main.route("/api/progress", methods=["POST"])
def update_progress():
    data = request.json
    user_id = data.get("user_id", "")
    progress = data.get("progress", {})

    if not user_id or not progress:
        return jsonify({"error": "Invalid data"}), 400

    # Placeholder: Save user progress to the database (or print for now)
    print(f"User {user_id} progress: {progress}")

    return jsonify({"message": "Progress updated successfully"}), 200


@main.route("/api/progress/<user_id>", methods=["GET"])
def get_progress(user_id):
    progress = Progress.query.filter_by(user_id=user_id).first()

    if not progress:
        return jsonify({"error": "No progress found for this user"}), 404

    return (
        jsonify(
            {
                "user_id": progress.user_id,
                "progress_data": progress.progress_data,
            }
        ),
        200,
    )
