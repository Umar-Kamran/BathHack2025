import React from "react";
import Chat from "../pages/chat"; // adjust the path if needed

type ChatModalProps = {
  onClose: () => void;
  branch: string; // Add branch prop
};

const ChatModal: React.FC<ChatModalProps> = ({ onClose, branch }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 duration-100">
      {/* Dimmed backdrop */}
      <div
        className="absolute inset-0 bg-black opacity-50"
        onClick={onClose}
      ></div>
      {/* Modal content */}
      <div className="relative bg-[var(--color-primary)] text-[var(--color-secondary)] rounded-lg shadow-lg p-6 z-10 transform transition-all duration-300 scale-100 max-w-md w-full">
        <Chat branch={branch}/>
      </div>
    </div>
  );
};

export default ChatModal;