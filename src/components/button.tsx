type buttonProps = {
    text: string;
    onClick: () => void;
    };

const Button = ({ text, onClick }: buttonProps) => {
    return (
        <button
            className="bg-secondary hover:bg-[var(--color-tertiary)] text-[var(--color-primary)] font-bold py-2 px-4 rounded duration-100 shadow-lg"
            onClick={onClick}
        >
            {text}
        </button>
    );
}

export default Button;