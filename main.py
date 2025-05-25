from flask import Flask, request, jsonify
import random

app = Flask(__name__)

# Example data – Replace or extend with real game logic later
ITEMS = ["Iron Sword", "Health Potion", "Magic Staff", "Leather Armor", "Gold Ring"]
ENEMIES = ["Goblin", "Skeleton", "Wolf", "Dark Knight", "Bandit"]
RARE_TIERS = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]

@app.route("/", methods=["GET"])
def home():
    return "Cardinal AI Backend is Running"

@app.route("/generate_enemy", methods=["POST"])
def generate_enemy():
    data = request.get_json()
    player_level = data.get("level", 1)

    enemy = {
        "name": random.choice(ENEMIES),
        "level": player_level + random.randint(-2, 5),
        "health": (player_level + random.randint(0, 5)) * 100,
        "damage": (player_level + random.randint(0, 3)) * 10,
    }
    return jsonify(enemy)

@app.route("/generate_item", methods=["POST"])
def generate_item():
    item = {
        "name": random.choice(ITEMS),
        "rarity": random.choice(RARE_TIERS),
    }
    return jsonify(item)

@app.route("/adjust_difficulty", methods=["POST"])
def adjust_difficulty():
    data = request.get_json()
    levels = data.get("playerLevels", [1])
    avg_level = sum(levels) / max(len(levels), 1)
    difficulty = "Easy"
    if avg_level > 25:
        difficulty = "Hard"
    elif avg_level > 10:
        difficulty = "Medium"
    return jsonify({"averageLevel": avg_level, "difficulty": difficulty})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Port can be changed in Render settings
