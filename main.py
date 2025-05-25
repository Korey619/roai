from flask import Flask, request, jsonify
import json
import os
import self_editor
import openai  # or any other LLM interface you use

app = Flask(__name__)

# Load persistent memory of the game state
if os.path.exists("game_memory.json"):
    with open("game_memory.json", "r") as f:
        memory = json.load(f)
else:
    memory = {"goals": ["make the game a better version of itself"], "history": []}

@app.route("/incoming_data", methods=["POST"])
def receive_data():
    data = request.json
    memory["history"].append({"event": "incoming_data", "data": data})
    return jsonify(generate_game_response(data))

def generate_game_response(data):
    # Example AI decision system
    prompt = f"""
Game Data: {json.dumps(data, indent=2)}
Goals: {memory['goals']}
How can we improve the game structure or content? Provide specific changes to the game logic, maps, or balance.
"""
    # Call the AI engine
    ai_output = call_ai_model(prompt)

    # Optionally modify self (main.py) if instructed
    if "MODIFY_SELF" in ai_output:
        self_editor.modify_main(ai_output)

    return {"response": ai_output}

def call_ai_model(prompt):
    # Replace with your LLM provider or API
    # Example using OpenAI:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an AI managing a game."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

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
