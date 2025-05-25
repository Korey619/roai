from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/build", methods=["POST"])
def build_game():
    data = request.get_json()

    # Decide what to build — you can make this dynamic or AI-based
    enemy = random.choice(data["enemies"])
    boss = random.choice(data["bosses"])
    chunk = random.choice(data["chunks"])

    return jsonify({
        "spawn_enemy": enemy,
        "spawn_boss": boss,
        "build_chunk": chunk
    })
