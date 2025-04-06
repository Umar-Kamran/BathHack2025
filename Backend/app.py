import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

# Initialize Firebase Admin with your service account key.
cred = credentials.Certificate("Backend/env/serviceAccount.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

app = Flask(__name__)
CORS(app)

@app.route('/get_conversation', methods=['POST'])
def get_conversation():
    """
    Expects a JSON payload with:
      - userId: The Firebase Auth user id.
      - branch: The branch identifier (branch name).
      
    Returns a JSON response containing:
      - npc_name: The name of the NPC (hard-coded here as "Kratos").
      - previous_messages: An array of conversation messages in the proper format.
    """
    data = request.json
    user_id = data.get("userId")
    branch_name = data.get("branch")
    if branch_name == "neev" or branch_name == "aadhav" or branch_name == "umar":
        response_data = {
        "npc_name": branch_name,
        "previous_messages": []
    }
        return jsonify(response_data)
    
    if not user_id or not branch_name:
        return jsonify({"error": "Missing userId or branch"}), 400

    # Reference to the conversations subcollection under the user's branch document.
    convo_ref = (
        db.collection("users")
          .document(user_id)
          .collection("branches")
          .document(branch_name)
          .collection("conversations")
    )

    # Retrieve conversation documents ordered by timestamp.
    # (Assuming each conversation document has a 'timestamp' field set when added)
    convo_docs = convo_ref.order_by("timestamp").stream()

    # Format conversation history as expected by the frontend.
    # Each message will be an object with a key "user" (if sender is not "AI")
    # or "npc" (if sender is "AI") and the message text.
    conversation_history = []
    for doc in convo_docs:
        convo = doc.to_dict()
        sender = convo.get("sender")
        text = convo.get("messageText", "")
        if sender.lower() == "ai":
            conversation_history.append({"npc": text})
        else:
            conversation_history.append({"user": text})
    
    name = "None"
    
    with open("Backend/gods.txt", "r") as f:
        gods = json.load(f)

        god_data = gods.get(branch_name)

        if god_data:
            name = god_data["name"]


    # Return only the NPC name and conversation history.
    response_data = {
        "npc_name": name,
        "previous_messages": conversation_history
    }
    
    return jsonify(response_data)


@app.route('/generate_response', methods=['POST'])
def generate_response():
    import time
    # Import your conversation module and create a conversation instance.
    from conversation import conversation

    data = request.json
    prompt = data.get("prompt", "")
    previous_messages = data.get("previous_messages", [])
    userId = data.get("user_id")       # Ensure this is provided in the payload
    branch = data.get("branch")       # Ensure this is provided in the payload


    conversation_instance = conversation(branch, previous_messages)
    
    # Generate the AI response (dummy logic; replace with your own as needed)
    response_text = conversation_instance.generate_response(prompt, previous_messages)

    if response_text[0] == "conversation":
        response_text = response_text[1]
    elif response_text[0] == "task":
        
        _,response_text, json_task = response_text
        print("Task JSON:", json_task)  # Debugging line to check the task JSON structure
        #add status ="active" to the task json
        json_task["status"] = "active"
        
        # Add the task to Firestore under the user's branch document.
        task_ref = (
            db.collection("users")
              .document(userId)
              .collection("branches")
              .document(branch)
              .collection("quests")
        )
        task_ref.add(json_task)  # Add the task JSON to Firestore

        try:
            print("Task added to Firestore.")
        except Exception as e:
            print("Error adding task to Firestore:", e)
    else:
        response_text = response_text[1]
    
    # Update Firestore conversation history if userId and branch are provided.
    if userId and branch:
        try:
            conv_collection = db.collection("users").document(userId) \
                                .collection("branches").document(branch) \
                                .collection("conversations")
            # Add the user's message.
            conv_collection.add({
                "sender": "User",
                "messageText": prompt,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            time.sleep(1)  # Optional: Sleep for a second to ensure the timestamp is different.
            # Add the AI's response.
            conv_collection.add({
                "sender": "AI",
                "messageText": response_text,
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            print("Conversation history updated in Firestore.")
        except Exception as e:
            print("Error updating conversation history:", e)

    return jsonify({"response": response_text})


def build_talent_tree(talents, unlocked_dict):
    # Build a dictionary of talentId -> talent object (including children list)
    talent_map = {}
    for talent in talents:
        talent_data = talent.to_dict()
        talent_data["talentId"] = talent.id
        # Mark as active if user unlocked it, otherwise false
        talent_data["isActive"] = unlocked_dict.get(talent.id, False)
        talent_data["children"] = []
        talent_map[talent.id] = talent_data

    # Build the tree by linking children talents to their parent
    tree = []
    for talent_id, talent_data in talent_map.items():
        parent_id = talent_data.get("parentTalent")
        if parent_id and parent_id in talent_map:
            talent_map[parent_id]["children"].append(talent_data)
        else:
            tree.append(talent_data)
    return tree

@app.route('/get_talent_tree', methods=['POST'])
def get_talent_tree():
    data = request.json
    user_id = data.get("userId")
    if not user_id:
        return jsonify({"error": "userId is required"}), 400

    # Query all global talents
    talents_ref = db.collection("talents")
    talents_snapshot = talents_ref.stream()
    talents = list(talents_snapshot)

    # Get the user's unlocked talents from their subcollection "unlockedTalents"
    unlocked_ref = db.collection("users").document(user_id).collection("unlockedTalents")
    unlocked_snapshot = unlocked_ref.stream()

    # Build a dict mapping talentId to isUnlocked status.
    unlocked_dict = {}
    for doc in unlocked_snapshot:
        doc_data = doc.to_dict()
        unlocked_dict[doc.id] = doc_data.get("isUnlocked", False)

    # Build a tree structure of talents
    talent_tree = build_talent_tree(talents, unlocked_dict)

    return jsonify({"talentTree": talent_tree})


if __name__ == '__main__':
    app.run(debug=True)
