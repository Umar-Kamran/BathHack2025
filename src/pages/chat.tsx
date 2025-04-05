import React, { useState, useEffect } from "react";

// Define the shape of a chat message
interface Message {
  id: number;
  sender: "ai" | "user";
  text: string;
}

const Chat: React.FC = () => {
  // Assume these are provided dynamically in your app.
  const userId = "user1"; // Example test user id
  const branch = "adventure"; // Example branch name

  // Local state for messages and input value.
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputValue, setInputValue] = useState("");

  // NPC name state; this will be updated from the API.
  const [npcName, setNpcName] = useState("Kratos");

  // Fetch conversation history when the component mounts.
  useEffect(() => {
    const fetchConversationHistory = async () => {
      try {
        const response = await fetch("http://localhost:5000/get_conversation", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId, branch }),
        });
        if (!response.ok) {
          console.error("Failed to fetch conversation history");
          return;
        }
        const data = await response.json();
        // Update the NPC name from the fetched data.
        setNpcName(data.npc_name);

        // Transform the conversation history into the local Message format.
        const initialMessages = data.previous_messages
          .map((msg: any, index: number) => {
            if (msg.npc) {
              return { id: Date.now() + index, sender: "ai", text: msg.npc };
            } else if (msg.user) {
              return { id: Date.now() + index, sender: "user", text: msg.user };
            }
            return null;
          })
          .filter((msg: Message | null): msg is Message => msg !== null);

        setMessages(initialMessages);
      } catch (error) {
        console.error("Error fetching conversation:", error);
      }
    };

    fetchConversationHistory();
  }, [userId, branch]);

  // Handle sending a message and receiving a response.
  const handleSendMessage = async () => {
    if (!inputValue.trim()) return;

    // Create and add the new user message.
    const userMessage: Message = {
      id: Date.now(),
      sender: "user",
      text: inputValue.trim(),
    };
    setMessages((prev) => [...prev, userMessage]);

    // Prepare the data for the Flask API, passing only conversation history and NPC name.
    const requestData = {
      npc_name: npcName,
      prompt: inputValue.trim(),
      previous_messages: messages.map((msg) =>
        msg.sender === "user" ? { user: msg.text } : { npc: msg.text }
      ),
      mode: "conversation",
      user_id: userId,
      branch: branch,
    };

    // Clear the input field.
    setInputValue("");

    try {
      const response = await fetch("http://localhost:5000/generate_response", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestData),
      });
      if (!response.ok) {
        console.error("Failed to fetch response from API");
        return;
      }
      const data = await response.json();
      const aiMessage: Message = {
        id: Date.now() + 1,
        sender: "ai",
        text: data.response,
      };

      // Append the AI's response to the messages state.
      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  return (
    <div className="flex justify-center items-center min-h-screen bg-gray-100">
      {/* Chat window container */}
      <div className="flex flex-col w-full max-w-md h-[80vh] bg-white shadow-lg rounded-md overflow-hidden">
        {/* Chat header displaying the NPC name */}
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
