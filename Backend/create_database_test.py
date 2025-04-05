import firebase_admin
from firebase_admin import credentials, firestore

# Initialize the Firebase Admin SDK with your service account key file.
cred = credentials.Certificate("env/serviceAccount.json")  # Replace with your key file path
firebase_admin.initialize_app(cred)

db = firestore.client()

# Define test users data
test_users = [
    {
        "userId": "user1",
        "displayName": "Alice",
        "userLevel": 2,
        "currentExperience": 150,
        "branches": [
            {
                "branchId": "adventure",
                "branchLevel": 1,
                "branchXP": 100,
                "quests": [
                    {
                        "taskTitle": "Find the lost sword",
                        "xpPoints": 200,
                        "tags": ["quest", "adventure"],
                        "status": "active"
                    },
                    {
                        "taskTitle": "Defeat the dragon",
                        "xpPoints": 300,
                        "tags": ["combat", "adventure"],
                        "status": "active"
                    }
                ],
                "conversations": [
                    {
                        "sender": "AI",
                        "messageText": "Welcome to your adventure branch!"
                    },
                    {
                        "sender": "User",
                        "messageText": "I'm ready to begin!"
                    }
                ]
            }
        ]
    },
    {
        "userId": "user2",
        "displayName": "Bob",
        "userLevel": 3,
        "currentExperience": 250,
        "branches": [
            {
                "branchId": "mystery",
                "branchLevel": 2,
                "branchXP": 200,
                "quests": [
                    {
                        "taskTitle": "Solve the ancient puzzle",
                        "xpPoints": 150,
                        "tags": ["puzzle", "mystery"],
                        "status": "active"
                    }
                ],
                "conversations": [
                    {
                        "sender": "AI",
                        "messageText": "Welcome to the mystery branch!"
                    }
                ]
            },
            {
                "branchId": "adventure",
                "branchLevel": 1,
                "branchXP": 80,
                "quests": [
                    {
                        "taskTitle": "Explore the hidden cave",
                        "xpPoints": 100,
                        "tags": ["exploration", "adventure"],
                        "status": "completed"
                    }
                ],
                "conversations": [
                    {
                        "sender": "AI",
                        "messageText": "This branch is full of surprises!"
                    }
                ]
            }
        ]
    },
    {
        "userId": "user3",
        "displayName": "Charlie",
        "userLevel": 1,
        "currentExperience": 50,
        "branches": [
            {
                "branchId": "exploration",
                "branchLevel": 1,
                "branchXP": 70,
                "quests": [
                    {
                        "taskTitle": "Climb the mountain",
                        "xpPoints": 120,
                        "tags": ["exploration", "challenge"],
                        "status": "active"
                    }
                ],
                "conversations": [
                    {
                        "sender": "AI",
                        "messageText": "The mountain awaits, are you prepared?"
                    }
                ]
            }
        ]
    }
]

# Iterate over each test user to create the documents and subcollections
for user in test_users:
    user_ref = db.collection("users").document(user["userId"])
    user_data = {
        "displayName": user["displayName"],
        "userLevel": user["userLevel"],
        "currentExperience": user["currentExperience"]
    }
    user_ref.set(user_data)
    print(f"Created user document for {user['displayName']}")

    # Create branches for the user
    for branch in user.get("branches", []):
        branch_ref = user_ref.collection("branches").document(branch["branchId"])
        branch_data = {
            "branchLevel": branch["branchLevel"],
            "branchXP": branch["branchXP"]
        }
        branch_ref.set(branch_data)
        print(f"  Created branch document '{branch['branchId']}' for {user['displayName']}")

        # Create quests subcollection for the branch
        for quest in branch.get("quests", []):
            quest_ref = branch_ref.collection("quests").document()  # Auto-generated quest ID
            quest_ref.set(quest)
            print(f"    Added quest '{quest['taskTitle']}' in branch '{branch['branchId']}' for {user['displayName']}")

        # Create conversations subcollection for the branch
        for convo in branch.get("conversations", []):
            convo_ref = branch_ref.collection("conversations").document()  # Auto-generated message ID
            convo_ref.set(convo)
            print(f"    Added conversation message from '{convo['sender']}' in branch '{branch['branchId']}' for {user['displayName']}")

print("Database setup complete with test users, branches, quests, and conversations!")
