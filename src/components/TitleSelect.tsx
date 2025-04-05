import React from "react";

type TitleSelectionModalProps = {
  titles: string[];
  onClose: () => void;
  onTitleSelect: (title: string) => void;  // New callback prop
};

const TitleSelect: React.FC<TitleSelectionModalProps> = ({ titles, onClose, onTitleSelect }) => {
  return (
    <div className="fixed inset-0 flex items-center justify-center z-50 duration-100">
      {/* Dimmed backdrop */}
      <div className="absolute inset-0 bg-black opacity-50" onClick={onClose}></div>
      {/* Modal content */}
      <div className="relative bg-[var(--color-primary)] text-[var(--color-secondary)] opacity-90 rounded-lg shadow-lg p-6 z-10 transform transition-all duration-300 scale-100">
        <h2 className="text-2xl font-bold mb-4">Select Your Title</h2>
        <ul>
          {titles.map((title, idx) => (
            <li
              key={idx}
              className="py-2 border-b last:border-b-0 cursor-pointer hover:bg-[#454a50] rounded"
              onClick={() => {
                onTitleSelect(title);
                onClose();
              }}
            >
              {title}
            </li>
          ))}
        </ul>
        <button
          className="mt-4 px-4 py-2 bg-[var(--color-secondary)] text-[var(--color-primary)] rounded"
          onClick={onClose}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default TitleSelect;