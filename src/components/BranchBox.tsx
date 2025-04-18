type branchboxProps = {
    text: string;
    onClick: () => void;
    icon: string;
}

const BranchBox = ({ text, onClick, icon }: branchboxProps) => {
    return (
        <div
            className="flex items-center bg-[var(--color-secondary)] hover:bg-[#4bba86] duration-200 text-[var(--color-primary)] text-2xl rounded p-4 cursor-pointer shadow-xl shadow-black"
            onClick={onClick}
        >
            <img
                src={icon}
                alt="icon"
                className="w-12 h-12 mr-2"
            />
            <span className="mr-auto">{text}</span>
            <button className="bg-primary border border-[var(--color-tertiary)] text-[var(--color-tertiary)] rounded-4xl px-2 py-1 items-center">+</button>
        </div>
    );
}

export default BranchBox;