from npc import Npc
class conversation:
    def __init__(self,  npc_name, chat, role, personality):
        self.npc = Npc(npc_name, chat, role, personality)

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
        response = self.npc.generate_response(prompt, previous_messages, quests, mode)
        # response = "test"
        self.npc.add_to_chat(f"user:{prompt}\n")
        self.npc.add_to_chat(f"npc:{response}\n")
        print(f"chat history: {self.npc.chat}")

        return response
    