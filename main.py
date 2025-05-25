from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    print("Received from Roblox:", data)

    # Example: respond with map-building instructions
    response = {
        "Actions": [
            {
                "Type": "PlaceModel",
                "Folder": "MapParts",
                "Model": "StoneWall",
                "Position": [0, 0, 0]
            },
            {
                "Type": "PlaceModel",
                "Folder": "EnemyModels",
                "Model": "Skeleton",
                "Position": [10, 0, -20]
            }
        ]
    }

    return jsonify(response)
