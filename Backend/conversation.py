from npc import Npc
import json
class conversation:
    def __init__(self,  branch, chat):
        def get_role_and_personality(branch):
            with open("Backend/gods.txt", "r") as f:
                gods = json.load(f)

            god_data = gods.get(branch)

            if god_data:
                return god_data["role"], god_data["personality"]
            else:
                return "Unknown", "Neutral"
        role, personality = get_role_and_personality(branch)

        for message in chat:
            print(message)
        self.npc = Npc(branch, chat, role, personality)

    def generate_response(self, prompt, previous_messages=None, quests=None, mode="conversation"):
        """
        Generate a response from the NPC based on the conversation context. adds the user and npc messages to the chat history.

        Parameters:
            prompt (str): The user's latest message.
            previous_messages (list): A list of dict messages representing the conversation history.
            quests (list/dict/str): The user's quest history.
            mode (str): "conversation" for normal chat or "task" for assigning a new quest.
        
        Returns:
            str: The NPC's response.
        """
        # response = self.npc.generate_response(prompt, previous_messages, quests, mode)
        response = "test"
        

        return response
    