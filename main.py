from flask import Flask, request, jsonify
import json
import os
import openai
import self_editor

app = Flask(__name__)

# Load OpenAI API key
try:
    with open("/etc/secrets/openai_api_key.txt", "r") as f:
        openai.api_key = f.read().strip()
except FileNotFoundError:
    print("WARNING: OpenAI API key file not found.")
    openai.api_key = os.getenv("OPENAI_API_KEY")

# Persistent memory
if os.path.exists("game_memory.json"):
    with open("game_memory.json", "r") as f:
        memory = json.load(f)
    memory.setdefault("goals", ["make the game a better version of itself"])
    memory.setdefault("history", [])
else:
    memory = {"goals": ["make the game a better version of itself"], "history": []}

@app.route("/generate", methods=["POST"])
def generate():
    try:
        data = request.json
        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        memory["history"].append({"event": "generate_request", "data": data})
        with open("game_memory.json", "w") as f:
            json.dump(memory, f, indent=2)

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
    goals = memory.get("goals", ["make the game a better version of itself"])
    prompt = f"""
Game Data: {json.dumps(data, indent=2)}
Goals: {goals}
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
        if not openai.api_key:
            raise Exception("OpenAI API key not set")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use free model
            messages=[
                {"role": "system", "content": "You are an AI managing a Roblox game."},
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
