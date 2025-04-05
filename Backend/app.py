from flask import Flask, request, jsonify
from flask_cors import CORS
from conversation import conversation  # adjust as necessary

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate_response', methods=['POST'])
def generate_response():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing JSON data"}), 400

    required_fields = ['npc_name', 'chat', 'role', 'personality', 'prompt']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

    npc_name = data['npc_name']
    chat = data['chat']
    role = data['role']
    personality = data['personality']
    prompt = data['prompt']
    previous_messages = data.get('previous_messages', None)
    quests = data.get('quests', None)
    mode = data.get('mode', "conversation")

    try:
        conv = conversation(npc_name, chat, role, personality)
        response_text = conv.generate_response(prompt, previous_messages, quests, mode)
        return jsonify({"response": response_text}), 200
    except Exception as e:
        print(f"Error generating response: {e}")  # Log the error for debugging
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
