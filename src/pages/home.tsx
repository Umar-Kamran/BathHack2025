import Button from "../components/button";
import GoogleLogin from "./GoogleLogin";
import { auth } from "../lib/firebase";
import { useAuthState } from "react-firebase-hooks/auth";


const Home: React.FC = () => {
    const [user] = useAuthState(auth)
    const isLoggedIn = !!user;

    const handleStatClick = () => {
        if (!isLoggedIn) {
            alert("Login to continue")
        }
        else {
            alert("do some stuff")
        }
    }

      return (
    <div className="min-h-screen bg-[var(--color-primary)] text-white p-4">
      <header className="flex justify-between items-center mb-8">
        <div>
            {/* logo here */}
        </div>
        <div className="flex-grow text-center p-4 mx-1">
          <h1 className="text-6xl font-bold text-[var(--color-secondary)]">{isLoggedIn ?"Level 6 Adept Engineer": "Level X Unkown..."}</h1>
        </div>
        {/* This is your login/logout button corner */}
        <div className="flex items-center">
            <GoogleLogin />
        </div>
      </header>
      <div className="grid grid-cols-3 gap-2 justify-centre justify-items-center mb-8">
        <div>
            <Button text="Talent Tree" onClick={() => alert("clicked")}></Button>
        </div>
        <div>
            <Button text="Select Title" onClick={() => alert("clicked")}></Button>
        </div>
        <div> 
            <Button text="Completed Quests" onClick={() => alert("clicked")}></Button>
        </div>
      </div>

      {/* Body: Stats Section */}
      {/* If not logged in, we apply opacity and disable pointer events */}
      <div
        className={`grid gap-4 ${
          !isLoggedIn ? "opacity-50 pointer-events-none" : ""
        }`}
      >
        {/* Example of a stat item */}
        <div
          className="flex items-center bg-[var(--color-secondary)] rounded p-4 cursor-pointer"
          onClick={handleStatClick}
        >
          <img
            src="/path/to/icon1.png"
            alt="Strength icon"
            className="w-6 h-6 mr-2"
          />
          <span className="mr-auto">Strength</span>
          <button className="bg-white text-black rounded px-2 py-1">+</button>
        </div>

        <div
          className="flex items-center bg-[var(--color-secondary)] rounded p-4 cursor-pointer"
          onClick={handleStatClick}
        >
          <img
            src="/path/to/icon2.png"
            alt="Strength icon"
            className="w-6 h-6 mr-2"
          />
          <span className="mr-auto">Strength</span>
          <button className="bg-white text-black rounded px-2 py-1">+</button>
        </div>

        <div
          className="flex items-center bg-[var(--color-secondary)] rounded p-4 cursor-pointer"
          onClick={handleStatClick}
        >
          <img
            src="/path/to/icon3.png"
            alt="Strength icon"
            className="w-6 h-6 mr-2"
          />
          <span className="mr-auto">Strength</span>
          <button className="bg-white text-black rounded px-2 py-1">+</button>
        </div>
      </div>
    </div>
  );
};

export default Home;