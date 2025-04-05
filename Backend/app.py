import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize Firebase Admin with your service account key.
cred = credentials.Certificate("env/serviceAccount.json")
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
    
    # In this example, we hard-code the NPC name as "Kratos".
    npc_name = "Kratos"
    
    # Return only the NPC name and conversation history.
    response_data = {
        "npc_name": npc_name,
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


if __name__ == '__main__':
    app.run(debug=True)
