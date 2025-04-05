import React, { useState } from "react";

// Define the shape of a chat message
interface Message {
  id: number;
  sender: "ai" | "user";
  text: string;
}

const Chat: React.FC = () => {
  // Constants for the conversation details (customize as needed)
  const npcName = "Kratos";
  const chatContext = ""; // You can add initial context here if needed
  const role = "Warrior NPC";
  const personality = "Stoic and wise";

  // Local state for messages and the input value
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");

  // Handle sending a message and getting the API response
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // Create a new user message
    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: inputValue.trim(),
    };

    // Update local state with the user message
    setMessages((prev) => [...prev, userMessage]);

    // Prepare data for the Flask API request.
    // We convert our local messages to a structure that the Python script expects.
    const requestData = {
      npc_name: npcName,
      chat: chatContext,
      role: role,
      personality: personality,
      prompt: inputValue.trim(),
      previous_messages: messages.map((msg) =>
        msg.sender === "user" ? { user: msg.text } : { npc: msg.text }
      ),
      mode: "conversation",
    };

    // Clear the input field
    setInputValue("");

    try {
      // Call the Flask API endpoint
      const response = await fetch("http://localhost:5000/generate_response", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      if (!response.ok) {
        console.error("Failed to fetch response from API");
        return;
      }

      // Parse the response JSON
      const data = await response.json();
      const aiMessage: Message = {
        id: Date.now() + 1,
        sender: "ai",
        text: data.response,
      };

      // Append the AI's response to the messages state
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      {/* Chat window container */}
      <div className="flex flex-col w-full max-w-md h-[80vh] bg-white shadow-lg rounded-md overflow-hidden">
        {/* Chat header */}
        <div className="px-4 py-2 bg-gray-200 text-gray-800 font-semibold">
          {npcName}
        </div>

        {/* Chat messages display */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => {
            const isAi = message.sender === "ai";
            return (
              <div
                key={message.id}
                className={`flex ${isAi ? "justify-start" : "justify-end"}`}
              >
                <div
                  className={`rounded-xl p-3 max-w-xs ${
                    isAi
                      ? "bg-gray-200 text-gray-800"
                      : "bg-blue-500 text-white"
                  }`}
                >
                  {message.text}
                </div>
              </div>
            );
          })}
        </div>

        {/* Input area for user messages */}
        <div className="flex p-3 border-t border-gray-200">
          <input
            type="text"
            className="flex-1 border border-gray-300 rounded-l-md px-3 py-2 focus:outline-none focus:ring-1 focus:ring-blue-500"
            placeholder="Type a message..."
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleSendMessage();
            }}
          />
          <button
            className="bg-blue-500 text-white px-4 py-2 rounded-r-md hover:bg-blue-600"
            onClick={handleSendMessage}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chat;
