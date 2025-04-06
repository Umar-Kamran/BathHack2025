import firebase_admin
from firebase_admin import credentials, firestore
import datetime

# Initialize the Firebase Admin SDK with your service account key file.
cred = credentials.Certificate("env/serviceAccount.json")  # Replace with your actual key file path
firebase_admin.initialize_app(cred)
db = firestore.client()

talents_data = [
    {
        "talentId": "t_physics",
        "talentName": "Physics",
        "description": "Covers fundamental principles of mechanics, electromagnetism, and quantum phenomena.",
        "requiredLevel": 2,
        "parentTalent": "t_maths",
        "quests": [
            {
                "questId": "q_physics1",
                "taskTitle": "Study Newton's Laws",
                "xpPoints": 100,
                "tags": ["physics", "mechanics"],
            },
            {
                "questId": "q_physics2",
                "taskTitle": "Experiment with Electromagnetism",
                "xpPoints": 150,
                "tags": ["physics", "electromagnetism"],
            },
            {
                "questId": "q_physics3",
                "taskTitle": "Analyze Quantum Experiments",
                "xpPoints": 200,
                "tags": ["physics", "quantum"],
            }
        ]
    },
    {
        "talentId": "t_maths",
        "talentName": "Maths",
        "description": "Enhances skills in algebra, calculus, geometry, and statistics.",
        "requiredLevel": 1,
        "parentTalent": None,
        "quests": [
            {
                "questId": "q_maths1",
                "taskTitle": "Solve Algebra Equations",
                "xpPoints": 90,
                "tags": ["maths", "algebra"],
            },
            {
                "questId": "q_maths2",
                "taskTitle": "Master Calculus Concepts",
                "xpPoints": 120,
                "tags": ["maths", "calculus"],
            },
            {
                "questId": "q_maths3",
                "taskTitle": "Explore Geometric Theorems",
                "xpPoints": 110,
                "tags": ["maths", "geometry"],
            }
        ]
    },
    {
        "talentId": "t_chemistry",
        "talentName": "Chemistry",
        "description": "Focuses on matter properties, reactions, and lab techniques in organic, inorganic, and physical chemistry.",
        "requiredLevel": 2,
        "parentTalent": "t_physics",
        "quests": [
            {
                "questId": "q_chem1",
                "taskTitle": "Learn the Periodic Table",
                "xpPoints": 80,
                "tags": ["chemistry", "elements"],
            },
            {
                "questId": "q_chem2",
                "taskTitle": "Conduct a Synthesis Reaction",
                "xpPoints": 140,
                "tags": ["chemistry", "synthesis"],
            },
            {
                "questId": "q_chem3",
                "taskTitle": "Analyze Chemical Bonds",
                "xpPoints": 130,
                "tags": ["chemistry", "bonds"],
            }
        ]
    },
    {
        "talentId": "t_biology",
        "talentName": "Biology",
        "description": "Explores the fundamentals of cellular biology, genetics, evolution, and ecology.",
        "requiredLevel": 1,
        "parentTalent": "t_maths",
        "quests": [
            {
                "questId": "q_bio1",
                "taskTitle": "Study Cell Structures",
                "xpPoints": 70,
                "tags": ["biology", "cells"],
            },
            {
                "questId": "q_bio2",
                "taskTitle": "Understand Genetic Inheritance",
                "xpPoints": 100,
                "tags": ["biology", "genetics"],
            },
            {
                "questId": "q_bio3",
                "taskTitle": "Examine Ecosystem Interactions",
                "xpPoints": 120,
                "tags": ["biology", "ecology"],
            }
        ]
    },
    {
        "talentId": "t_compsci",
        "talentName": "Computer Science",
        "description": "Covers programming fundamentals, data structures, algorithms, and software design.",
        "requiredLevel": 2,
        "parentTalent": "t_electronics",
        "quests": [
            {
                "questId": "q_cs1",
                "taskTitle": "Learn Python Programming",
                "xpPoints": 100,
                "tags": ["computerscience", "programming"],
            },
            {
                "questId": "q_cs2",
                "taskTitle": "Master Data Structures",
                "xpPoints": 130,
                "tags": ["computerscience", "data structures"],
            },
            {
                "questId": "q_cs3",
                "taskTitle": "Design an Algorithm",
                "xpPoints": 150,
                "tags": ["computerscience", "algorithms"],
            }
        ]
    },
    {
        "talentId": "t_electronics",
        "talentName": "Electronics",
        "description": "Focuses on circuit design, signal processing, and electronic device principles.",
        "requiredLevel": 3,
        "parentTalent": "t_maths",
        "quests": [
            {
                "questId": "q_elec1",
                "taskTitle": "Build a Simple Circuit",
                "xpPoints": 110,
                "tags": ["electronics", "circuits"],
            },
            {
                "questId": "q_elec2",
                "taskTitle": "Study Signal Processing",
                "xpPoints": 140,
                "tags": ["electronics", "signals"],
            },
            {
                "questId": "q_elec3",
                "taskTitle": "Design an Amplifier",
                "xpPoints": 160,
                "tags": ["electronics", "amplifiers"],
            }
        ]
    },
    {
        "talentId": "t_egypt",
        "talentName": "Egyptian History",
        "description": "Delves into ancient Egypt's culture, architecture, and historical events.",
        "requiredLevel": 1,
        "parentTalent": None,
        "quests": [
            {
                "questId": "q_egypt1",
                "taskTitle": "Study the Pyramids",
                "xpPoints": 90,
                "tags": ["egypt", "pyramids"],
            },
            {
                "questId": "q_egypt2",
                "taskTitle": "Learn about the Pharaohs",
                "xpPoints": 100,
                "tags": ["egypt", "pharaohs"],
            },
            {
                "questId": "q_egypt3",
                "taskTitle": "Explore Ancient Egyptian Culture",
                "xpPoints": 110,
                "tags": ["egypt", "culture"],
            }
        ]
    }
]

# Create global talents in the "talents" collection.
for talent in talents_data:
    talent_ref = db.collection("talents").document(talent["talentId"])
    talent_data = {
        "talentName": talent["talentName"],
        "description": talent["description"],
        "requiredLevel": talent["requiredLevel"],
        "parentTalent": talent["parentTalent"]
    }
    talent_ref.set(talent_data)
    print(f"Created talent document: {talent['talentName']}")
    
    # Create talent-specific quests subcollection.
    for quest in talent.get("quests", []):
        tq_ref = talent_ref.collection("talent_quests").document(quest["questId"])
        tq_ref.set(quest)
        print(f"  Added talent quest '{quest['taskTitle']}' for talent '{talent['talentName']}'")

# --- Test Users Data ---
test_users = [
  {
    "userId": "Yo1dpGES7ZOHxKMBTkhDZ7EKPNC2",
    "displayName": "Umar",
    "userLevel": 3,
    "currentExperience": 350,
    "titles": ["Epic Adventurer", "Master Explorer"],
    "branches": [
      {
        "branchId": "strength",
        "branchLevel": 2,
        "branchXP": 150,
        "quests": [
          {
            "taskTitle": "Do 30 pushups",
            "xpPoints": 50,
            "tags": ["strength", "exercise"],
            "status": "active"
          },
          {
            "taskTitle": "Run 2 km",
            "xpPoints": 70,
            "tags": ["strength", "cardio"],
            "status": "active"
          },
          {
            "taskTitle": "Hold a plank for 1 minute",
            "xpPoints": 40,
            "tags": ["strength", "core"],
            "status": "active"
          },
          {
            "taskTitle": "Perform 20 squats",
            "xpPoints": 50,
            "tags": ["strength", "legs"],
            "status": "active"
          }
        ],
<<<<<<< HEAD
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Building strength takes consistent effort. Push your limits safely and enjoy your progress."
          },
          {
            "sender": "User",
            "messageText": "I feel the burn and I'm ready to push myself harder."
          },
          {
            "sender": "AI",
            "messageText": "Remember to warm up properly and keep your form in check for maximum benefit."
          }
=======
        "talents": [
            {
                "talentId": "t_physics",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_physics1", "status": "active"},
                    {"questId": "q_physics2", "status": "active"},
                    {"questId": "q_physics3", "status": "active"}
                ],
                "unlockedConversations": []
            },
            {
                "talentId": "t_maths",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_maths1", "status": "active"},
                    {"questId": "q_maths2", "status": "active"},
                    {"questId": "q_maths3", "status": "active"}
                ],
                "unlockedConversations": []
            },
            {
                "talentId": "t_chemistry",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_chem1", "status": "active"},
                    {"questId": "q_chem2", "status": "active"},
                    {"questId": "q_chem3", "status": "active"}
                ],
                "unlockedConversations": []
            },
            {
                "talentId": "t_biology",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_bio1", "status": "active"},
                    {"questId": "q_bio2", "status": "active"},
                    {"questId": "q_bio3", "status": "active"}
                ],
                "unlockedConversations": []
            },
            {
                "talentId": "t_compsci",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_cs1", "status": "active"},
                    {"questId": "q_cs2", "status": "active"},
                    {"questId": "q_cs3", "status": "active"}
                ],
                "unlockedConversations": []
            },
            {
                "talentId": "t_electronics",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_elec1", "status": "active"},
                    {"questId": "q_elec2", "status": "active"},
                    {"questId": "q_elec3", "status": "active"}
                ],
                "unlockedConversations": []
            },
            {
                "talentId": "t_egypt",
                "isUnlocked": True,
                "quests": [
                    {"questId": "q_egypt1", "status": "active"},
                    {"questId": "q_egypt2", "status": "active"},
                    {"questId": "q_egypt3", "status": "active"}
                ],
                "unlockedConversations": []
            }
>>>>>>> 297f8a927f217dc5dadd69fe17d706d76bb59df6
        ]
      },
      {
        "branchId": "knowledge",
        "branchLevel": 2,
        "branchXP": 140,
        "quests": [
          {
            "taskTitle": "Read a chapter of a book",
            "xpPoints": 60,
            "tags": ["knowledge", "reading"],
            "status": "active"
          },
          {
            "taskTitle": "Learn 10 new words",
            "xpPoints": 40,
            "tags": ["knowledge", "vocabulary"],
            "status": "active"
          },
          {
            "taskTitle": "Watch an educational documentary",
            "xpPoints": 80,
            "tags": ["knowledge", "learning"],
            "status": "active"
          },
          {
            "taskTitle": "Solve a brain teaser",
            "xpPoints": 50,
            "tags": ["knowledge", "puzzle"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Every page you read expands your horizon. Embrace the journey of learning."
          },
          {
            "sender": "User",
            "messageText": "I love discovering new ideas and challenging my intellect."
          },
          {
            "sender": "AI",
            "messageText": "Stay curious and let every question lead you to new insights."
          }
        ]
      },
      {
        "branchId": "health",
        "branchLevel": 1,
        "branchXP": 100,
        "quests": [
          {
            "taskTitle": "Eat 6 pieces of fruit",
            "xpPoints": 30,
            "tags": ["health", "nutrition"],
            "status": "active"
          },
          {
            "taskTitle": "Drink 2 liters of water",
            "xpPoints": 20,
            "tags": ["health", "hydration"],
            "status": "active"
          },
          {
            "taskTitle": "Meditate for 15 minutes",
            "xpPoints": 40,
            "tags": ["health", "mindfulness"],
            "status": "active"
          },
          {
            "taskTitle": "Take a 30-minute walk",
            "xpPoints": 50,
            "tags": ["health", "activity"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Good health is the foundation of all progress. Small healthy choices lead to big changes."
          },
          {
            "sender": "User",
            "messageText": "I'm committed to making choices that nourish my body and mind."
          },
          {
            "sender": "AI",
            "messageText": "Keep track of your habits, and soon you'll see the benefits of a balanced lifestyle."
          }
        ]
      }
    ],
    "talents": [
      {
        "talentId": "t_physics",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_physics1", "status": "active"},
          {"questId": "q_physics2", "status": "active"},
          {"questId": "q_physics3", "status": "active"}
        ],
        "unlockedConversations": []
      },
      {
        "talentId": "t_maths",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_maths1", "status": "active"},
          {"questId": "q_maths2", "status": "active"},
          {"questId": "q_maths3", "status": "active"}
        ],
        "unlockedConversations": []
      },
      {
        "talentId": "t_chemistry",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_chem1", "status": "active"},
          {"questId": "q_chem2", "status": "active"},
          {"questId": "q_chem3", "status": "active"}
        ],
        "unlockedConversations": []
      },
      {
        "talentId": "t_biology",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_bio1", "status": "active"},
          {"questId": "q_bio2", "status": "active"},
          {"questId": "q_bio3", "status": "active"}
        ],
        "unlockedConversations": []
      },
      {
        "talentId": "t_compsci",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_cs1", "status": "active"},
          {"questId": "q_cs2", "status": "active"},
          {"questId": "q_cs3", "status": "active"}
        ],
        "unlockedConversations": []
      },
      {
        "talentId": "t_electronics",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_elec1", "status": "active"},
          {"questId": "q_elec2", "status": "active"},
          {"questId": "q_elec3", "status": "active"}
        ],
        "unlockedConversations": []
      },
      {
        "talentId": "t_egypt",
        "isUnlocked": True,
        "quests": [
          {"questId": "q_egypt1", "status": "active"},
          {"questId": "q_egypt2", "status": "active"},
          {"questId": "q_egypt3", "status": "active"}
        ],
        "unlockedConversations": []
      }
    ]
  },
  {
    "userId": "8AJGDGuUoubk3uqDxhHPKzqvGl13",
    "displayName": "Neev",
    "userLevel": 4,
    "currentExperience": 500,
    "titles": ["Mystery Solver", "Scholar of the Arcane"],
    "branches": [
      {
        "branchId": "strength",
        "branchLevel": 3,
        "branchXP": 200,
        "quests": [
          {
            "taskTitle": "Do 30 pushups",
            "xpPoints": 50,
            "tags": ["strength", "exercise"],
            "status": "active"
          },
          {
            "taskTitle": "Run 2 km",
            "xpPoints": 70,
            "tags": ["strength", "cardio"],
            "status": "active"
          },
          {
            "taskTitle": "Hold a plank for 1 minute",
            "xpPoints": 40,
            "tags": ["strength", "core"],
            "status": "active"
          },
          {
            "taskTitle": "Perform 20 squats",
            "xpPoints": 50,
            "tags": ["strength", "legs"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Building strength takes consistent effort. Push your limits safely and enjoy your progress."
          },
          {
            "sender": "User",
            "messageText": "I’m ready to challenge my body with some intense exercises."
          },
          {
            "sender": "AI",
            "messageText": "Stay focused and remember that every rep counts towards a stronger you."
          }
        ]
      },
      {
        "branchId": "knowledge",
        "branchLevel": 3,
        "branchXP": 180,
        "quests": [
          {
            "taskTitle": "Read a chapter of a book",
            "xpPoints": 60,
            "tags": ["knowledge", "reading"],
            "status": "active"
          },
          {
            "taskTitle": "Learn 10 new words",
            "xpPoints": 40,
            "tags": ["knowledge", "vocabulary"],
            "status": "active"
          },
          {
            "taskTitle": "Watch an educational documentary",
            "xpPoints": 80,
            "tags": ["knowledge", "learning"],
            "status": "active"
          },
          {
            "taskTitle": "Solve a brain teaser",
            "xpPoints": 50,
            "tags": ["knowledge", "puzzle"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Every page you read expands your horizon. Embrace the journey of learning."
          },
          {
            "sender": "User",
            "messageText": "I thrive on challenging my mind and exploring new ideas."
          },
          {
            "sender": "AI",
            "messageText": "Keep asking questions—each answer is a stepping stone to deeper insight."
          }
        ]
      },
      {
        "branchId": "health",
        "branchLevel": 2,
        "branchXP": 160,
        "quests": [
          {
            "taskTitle": "Eat 6 pieces of fruit",
            "xpPoints": 30,
            "tags": ["health", "nutrition"],
            "status": "active"
          },
          {
            "taskTitle": "Drink 2 liters of water",
            "xpPoints": 20,
            "tags": ["health", "hydration"],
            "status": "active"
          },
          {
            "taskTitle": "Meditate for 15 minutes",
            "xpPoints": 40,
            "tags": ["health", "mindfulness"],
            "status": "active"
          },
          {
            "taskTitle": "Take a 30-minute walk",
            "xpPoints": 50,
            "tags": ["health", "activity"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Good health is the foundation of all progress. Small healthy choices lead to big changes."
          },
          {
            "sender": "User",
            "messageText": "I’m focusing on habits that boost both my energy and well-being."
          },
          {
            "sender": "AI",
            "messageText": "Excellent! Tracking your hydration and nutrition is key to a balanced lifestyle."
          }
        ]
      }
    ],
    "talents": [
      {
        "talentId": "t_maths",
        "isUnlocked": True,
        "quests": [
          {
            "questId": "q_maths1",
            "status": "completed"
          },
          {
            "questId": "q_maths3",
            "status": "active"
          }
        ],
        "unlockedConversations": [
          {
            "sender": "AI",
            "messageText": "Your mathematical prowess unlocks new dimensions of reasoning."
          },
          {
            "sender": "User",
            "messageText": "Every equation is a window into the hidden order of the cosmos."
          },
          {
            "sender": "AI",
            "messageText": "Continue to solve, and let the beauty of numbers guide your path."
          }
        ]
      },
      {
        "talentId": "t_electronics",
        "isUnlocked": True,
        "quests": [
          {
            "questId": "q_elec1",
            "status": "completed"
          },
          {
            "questId": "q_elec3",
            "status": "active"
          }
        ],
        "unlockedConversations": [
          {
            "sender": "AI",
            "messageText": "You have mastered the basics of electronics; now innovate and create."
          },
          {
            "sender": "User",
            "messageText": "I am ready to design circuits that challenge conventional boundaries."
          },
          {
            "sender": "AI",
            "messageText": "Harness your ingenuity to turn ideas into groundbreaking inventions."
          }
        ]
      },
      {
        "talentId": "t_egypt",
        "isUnlocked": False,
        "quests": [
          {
            "questId": "q_egypt2",
            "status": "active"
          }
        ],
        "unlockedConversations": []
      }
    ]
  },
  {
    "userId": "user3",
    "displayName": "Charlie",
    "userLevel": 2,
    "currentExperience": 200,
    "titles": ["Rookie Explorer", "Aspiring Scholar"],
    "branches": [
      {
        "branchId": "strength",
        "branchLevel": 1,
        "branchXP": 80,
        "quests": [
          {
            "taskTitle": "Do 30 pushups",
            "xpPoints": 50,
            "tags": ["strength", "exercise"],
            "status": "active"
          },
          {
            "taskTitle": "Run 2 km",
            "xpPoints": 70,
            "tags": ["strength", "cardio"],
            "status": "active"
          },
          {
            "taskTitle": "Hold a plank for 1 minute",
            "xpPoints": 40,
            "tags": ["strength", "core"],
            "status": "active"
          },
          {
            "taskTitle": "Perform 20 squats",
            "xpPoints": 50,
            "tags": ["strength", "legs"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Building strength is about steady progress. Every workout counts!"
          },
          {
            "sender": "User",
            "messageText": "I'm excited to get started and see improvements in my fitness."
          },
          {
            "sender": "AI",
            "messageText": "Keep a consistent schedule and always listen to your body."
          }
        ]
      },
      {
        "branchId": "knowledge",
        "branchLevel": 1,
        "branchXP": 90,
        "quests": [
          {
            "taskTitle": "Read a chapter of a book",
            "xpPoints": 60,
            "tags": ["knowledge", "reading"],
            "status": "active"
          },
          {
            "taskTitle": "Learn 10 new words",
            "xpPoints": 40,
            "tags": ["knowledge", "vocabulary"],
            "status": "active"
          },
          {
            "taskTitle": "Watch an educational documentary",
            "xpPoints": 80,
            "tags": ["knowledge", "learning"],
            "status": "active"
          },
          {
            "taskTitle": "Solve a brain teaser",
            "xpPoints": 50,
            "tags": ["knowledge", "puzzle"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Every new fact you learn adds to your wisdom. Keep exploring!"
          },
          {
            "sender": "User",
            "messageText": "I’m eager to dive into a new book and expand my horizons."
          },
          {
            "sender": "AI",
            "messageText": "Great! Let your curiosity guide you through every page and puzzle."
          }
        ]
      },
      {
        "branchId": "health",
        "branchLevel": 1,
        "branchXP": 70,
        "quests": [
          {
            "taskTitle": "Eat 6 pieces of fruit",
            "xpPoints": 30,
            "tags": ["health", "nutrition"],
            "status": "active"
          },
          {
            "taskTitle": "Drink 2 liters of water",
            "xpPoints": 20,
            "tags": ["health", "hydration"],
            "status": "active"
          },
          {
            "taskTitle": "Meditate for 15 minutes",
            "xpPoints": 40,
            "tags": ["health", "mindfulness"],
            "status": "active"
          },
          {
            "taskTitle": "Take a 30-minute walk",
            "xpPoints": 50,
            "tags": ["health", "activity"],
            "status": "active"
          }
        ],
        "conversations": [
          {
            "sender": "AI",
            "messageText": "Maintaining good health is key to enjoying every adventure."
          },
          {
            "sender": "User",
            "messageText": "I’m ready to incorporate more healthy habits into my day."
          },
          {
            "sender": "AI",
            "messageText": "Every small step toward health builds a better tomorrow."
          }
        ]
      }
    ],
    "talents": [
      {
        "talentId": "t_biology",
        "isUnlocked": True,
        "quests": [
          {
            "questId": "q_bio1",
            "status": "completed"
          },
          {
            "questId": "q_bio3",
            "status": "active"
          }
        ],
        "unlockedConversations": [
          {
            "sender": "AI",
            "messageText": "Your connection to the living world deepens with every discovery."
          },
          {
            "sender": "User",
            "messageText": "I feel the pulse of nature guiding my every step."
          },
          {
            "sender": "AI",
            "messageText": "Let your curiosity drive you to explore the wonders of life."
          }
        ]
      },
      {
        "talentId": "t_compsci",
        "isUnlocked": False,
        "quests": [
          {
            "questId": "q_cs2",
            "status": "active"
          }
        ],
        "unlockedConversations": []
      }
    ]
  }
]



# Create user documents and their unlocked talents.
for user in test_users:
    # Create the user document in the "users" collection.
    user_ref = db.collection("users").document(user["userId"])
    user_data = {
        "displayName": user["displayName"],
        "userLevel": user["userLevel"],
        "currentExperience": user["currentExperience"],
        "titles": user.get("titles", [])
    }
    user_ref.set(user_data)
    print(f"Created user document for {user['displayName']} with titles: {user_data['titles']}")

    # Create branches for the user.
    for branch in user.get("branches", []):
        branch_ref = user_ref.collection("branches").document(branch["branchId"])
        branch_data = {
            "branchLevel": branch["branchLevel"],
            "branchXP": branch["branchXP"]
        }
        branch_ref.set(branch_data)
        print(f"  Created branch document '{branch['branchId']}' for {user['displayName']}")

        # Create quests subcollection for the branch.
        for quest in branch.get("quests", []):
            quest_ref = branch_ref.collection("quests").document()  # Auto-generated quest ID.
            quest_ref.set(quest)
            print(f"    Added quest '{quest['taskTitle']}' in branch '{branch['branchId']}' for {user['displayName']}")

        # Create conversations subcollection for the branch.
        for convo in branch.get("conversations", []):
            convo_ref = branch_ref.collection("conversations").document()  # Auto-generated conversation ID.
            conversation_data = {
                "sender": convo["sender"],
                "messageText": convo["messageText"],
                "timestamp": datetime.datetime.utcnow().isoformat()
            }
            convo_ref.set(conversation_data)
            print(f"    Added conversation from '{convo['sender']}' in branch '{branch['branchId']}' for {user['displayName']}")

    # Create the "unlockedTalents" subcollection for the user.
    for talent in user.get("talents", []):
        unlocked_ref = user_ref.collection("unlockedTalents").document(talent["talentId"])
        unlocked_data = {
            "talentId": talent["talentId"],
            "isUnlocked": talent["isUnlocked"]
        }
        unlocked_ref.set(unlocked_data)
        print(f"  Set unlocked status for talent '{talent['talentId']}' to {talent['isUnlocked']} for user {user['displayName']}")

        # If the talent is unlocked, add its conversations subcollection.
        if talent["isUnlocked"]:
            for convo in talent.get("unlockedConversations", []):
                utc_ref = unlocked_ref.collection("unlocked_talent_conversations").document()
                utc_data = {
                    "sender": convo["sender"],
                    "messageText": convo["messageText"],
                    "timestamp": datetime.datetime.utcnow().isoformat()
                }
                utc_ref.set(utc_data)
                print(f"    Added unlocked talent conversation from '{convo['sender']}' for talent '{talent['talentId']}' for user {user['displayName']}")
            
            # Also add talent-specific quest status if provided.
            for tquest in talent.get("quests", []):
                tq_user_ref = unlocked_ref.collection("quests").document(tquest["questId"])
                tq_user_ref.set(tquest)
                print(f"    Updated talent quest '{tquest['questId']}' status for talent '{talent['talentId']}' for user {user['displayName']}")

print("Database setup complete with test users, global talents, and unlocked talent conversations!")
