from npc import Npc
class conversation:
    def __init__(self,  npc_name, chat, role, personality):
        self.npc = Npc(npc_name, chat, role, personality)

    def generate_response(self, prompt, previous_messages=None, quests=None, mode="conversation"):
        """
        Generate a response from the NPC based on the conversation context.

        Parameters:
            prompt (str): The user's latest message.
            previous_messages (list): A list of dict messages representing the conversation history.
            quests (list/dict/str): The user's quest history.
            mode (str): "conversation" for normal chat or "task" for assigning a new quest.
        
        Returns:
            str: The NPC's response.
        """
        response = self.npc.generate_response(prompt, previous_messages, quests, mode)
        self.npc.add_to_chat({"user":prompt})
        self.npc.add_to_chat({"npc":response})

        return response