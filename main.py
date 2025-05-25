from flask import Flask, request, jsonify
import json
import os
import self_editor
import openai  # Make sure it's installed and working

app = Flask(__name__)

# Load persistent memory of the game state
if os.path.exists("game_memory.json"):
    with open("game_memory.json", "r") as f:
        memory = json.load(f)
else:
    memory = {"goals": ["make the game a better version of itself"], "history": []}

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        if data is None:
            return jsonify({"error": "No JSON data received"}), 400

        memory["history"].append({"event": "generate_request", "data": data})
        print("[INCOMING DATA]:", json.dumps(data, indent=2))

        response_data = generate_game_response(data)
        print("[RESPONSE DATA]:", response_data)

        return jsonify(response_data)
    except Exception as e:
        import traceback
        print("[ERROR in /generate]:", str(e))
        print(traceback.format_exc())
        return jsonify({"error": "Internal server error", "details": str(e)}), 500

def generate_game_response(data):
    prompt = f"""
Game Data: {json.dumps(data, indent=2)}
Goals: {memory['goals']}
How can we improve the game structure or content? Provide specific changes to the game logic, maps, or balance.
"""
    print("[AI PROMPT]:", prompt)

    ai_output = call_ai_model(prompt)

    if "MODIFY_SELF" in ai_output:
        print("[SELF-EDIT TRIGGERED]")
        self_editor.modify_main(ai_output)

    return {
        "SpawnBoss": {
            "Name": "DemonBoss",
            "Position": {"X": 0, "Y": 10, "Z": 0}
        },
        "RawAIResponse": ai_output
    }

def call_ai_model(prompt):
    try:
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise Exception("OPENAI_API_KEY not set")

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI managing a game."},
                {"role": "user", "content": prompt}
            ]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        import traceback
        print("[AI ERROR]:", str(e))
        print(traceback.format_exc())
        return "AI failed to respond properly"

@app.route("/self_improve", methods=["POST"])
def self_improve():
    prompt = """
Review the current state of main.py and suggest improvements to make the game smarter, more efficient, or more fun.
Always align changes to the main directive: 'Make the game a better version of itself.'
Respond with specific Python code changes.
"""
    ai_response = call_ai_model(prompt)
    self_editor.modify_main(ai_response)
    return jsonify({"status": "improvement triggered", "details": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
