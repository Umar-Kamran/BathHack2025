#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import json
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()
api_key = os.getenv('API_KEY')

class Npc:
    def __init__(self, name, chat, role, personality, branch):
        self.name = name
        self.chat = chat
        self.role = role
        self.personality = personality
        self.branch = branch
        self.openai = OpenAI(api_key=api_key, base_url="https://hack.funandprofit.ai/api/providers/openai/v1")

    def determine_mode(self, prompt):
        """
        Determine the mode for the current prompt by asking the OpenAI chat API
        to decide if the prompt is a task assignment or a conversation.
        Returns:
            str: "task" or "conversation"
        """
        mode_instruction = (
            "Decide whether the following user prompt is asking to be given task assignment or a conversation/or explanation of a task. "
            "Respond with exactly one word: either 'task' or 'conversation'."
        )
        messages = [
            {"role": "system", "content": mode_instruction},
            {"role": "user", "content": prompt}
        ]
        response = self.openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=10,
            temperature=0.0,
        )
        mode = response.choices[0].message.content.strip().lower()
        print("Mode determined by OpenAI API:", mode)  # Debugging line to check the mode response
        # Fallback to conversation if the response is unexpected
        
        if "task" in mode:
            return "task"
        return "conversation"
    
    def generate_response(self, prompt, previous_messages=None, quests=None, ):
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

        mode = self.determine_mode(prompt)
        # Build the system instruction
        system_message = (
            f"You are {self.name}, a {self.role} Greek god with a {self.personality} personality. Your task is to assist the user in their journey relating to {self.branch}. "
        )
        
        if mode == "task":
            system_message += (
                "to assign a task, provide a short comment explaining the context and what to do, then on a new line output a delimiter '### TASK JSON START', "
                "followed by a valid JSON representation of this task. The JSON must include the keys 'taskTitle', 'duration' (in minutes),  'tags'(descriptive words, MAX 2 WORDS) and 'xpPoints'. "
                "Ensure that the JSON is valid and can be parsed. End the JSON with '### TASK JSON END'. "
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
            model="gpt-4o-mini",  # Change from "o3-mini" to "gpt-4o-mini"
            messages=messages,
            max_tokens=150,  # Change from max_completion_tokens to max_tokens
            temperature=0.7
        )
        print("Response from OpenAI API:", response)  # Debugging line to check the response
        if mode == "task":
            # Adjust the task output to ensure it is a valid JSON format.
            task_output = response.choices[0].message.content.strip()
            comment, task_json = self.adjust_task_output(task_output)

            if task_json:
                return mode, comment, task_json
            else:
                return "conversation", task_output, None  # Fallback to conversation if JSON parsing fails
        else:
            return mode, response.choices[0].message.content.strip()
    
    def adjust_task_output(self, task_output):
        """
        Adjust the task output to ensure it is a valid JSON format.
        """
        # Remove any unwanted characters or lines before the JSON output
        if "### TASK JSON START" in task_output:
            comment, task_output = task_output.split("### TASK JSON START")

        if "### TASK JSON END" in task_output:
            task_output = task_output.split("### TASK JSON END")[0]
        # Attempt to parse the JSON output
        try:
            task_json = json.loads(task_output.strip())
            return comment, task_json
        except json.JSONDecodeError:
            print("Failed to parse task JSON:", task_output)
            return "", None
