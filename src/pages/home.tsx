import Button from "../components/button";

const Home = () => {
    const handleClick = () => {
        alert("Button clicked!");
    };

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <h1 className="text-4xl font-bold mb-4">Welcome to BathHack 2025</h1>
            <p className="text-lg mb-8 text-blue-600">This is a simple example of a React component.</p>
            <Button text="Click Me!" onClick={handleClick} />
        </div>
    );
}

export default Home;