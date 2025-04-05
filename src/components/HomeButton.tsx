type buttonProps = {
  text: string;
  onClick: () => void;
};

const Button = ({ text, onClick }: buttonProps) => {
  return (
    <button
      className="bg-[var(--color-secondary)] text-[var(--color-primary)] hover:text-[var(--color-tertiary)] text-3xl py-3 px-20 rounded duration-300 shadow-lg shadow-black"
      onClick={onClick}
    >
      {text}
    </button>
  );
};

export default Button;
