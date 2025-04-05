#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import json
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('API_KEY')

class Npc:
    def __init__(self, name, chat, role, personality):
        self.name = name
        self.chat = chat
        self.role = role
        self.personality = personality
        self.openai = OpenAI(api_key=api_key, base_url="https://hack.funandprofit.ai/api/providers/openai/v1")

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
        # Build the system instruction
        system_message = (
            f"You are {self.name}, a {self.role} Greek god with a {self.personality} personality. "
        )
        
        if mode == "task":
            system_message += (
                "When assigning a task, provide a short comment, then on a new line output a delimiter '### TASK JSON START', "
                "followed by a valid JSON representation of the task. The JSON must include the keys 'title', 'duration' (in minutes), and 'activity_type'. "
                "Ensure that the JSON is valid and can be parsed."
            )
        else:
            system_message += (
                "Engage in thoughtful conversation and provide guidance if the user asks for help with tasks."
            )
        
        if quests:
            # Format quests as a JSON string if not already a string.
            if not isinstance(quests, str):
                try:
                    quests_str = json.dumps(quests)
                except Exception:
                    quests_str = str(quests)
            else:
                quests_str = quests
            system_message += f" The user's quest history is: {quests_str}."
        
        # Build the conversation messages
        messages = [{"role": "system", "content": system_message}]
        if previous_messages and isinstance(previous_messages, list):
            messages.extend(previous_messages)
        messages.append({"role": "user", "content": prompt})
        
        # Make the API call to generate the response.
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )
        print("Response from OpenAI API:", response)  # Debugging line to check the API response
        return response.choices[0].message.content.strip()
    
    def add_to_chat(self, message):
        """
        Add a message to the chat history.

        Parameters:
            message (dict): A dictionary containing the message to add.
        """
        self.chat += (message)
