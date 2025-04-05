import Button from "../components/HomeButton";
import GoogleLogin from "./GoogleLogin";
import BranchBox from "../components/BranchBox"; // Import BranchBox
import { auth } from "../lib/firebase";
import { useAuthState } from "react-firebase-hooks/auth";

const Home: React.FC = () => {
  const [user] = useAuthState(auth);
  const isLoggedIn = !!user;

  const handleStatClick = () => {
    if (!isLoggedIn) {
      alert("Login to continue");
    } else {
      alert("do some stuff");
    }
  };

  return (
    <div className="min-h-screen bg-[var(--color-primary)] text-white p-4">
      <header className="grid grid-cols-3 items-center mb-8">
        <div className="justify-start">{/* logo here */}</div>
        <div className="flex justify-center text-center p-4 mx-1">
          <h1 className="text-6xl font-bold text-[var(--color-secondary)]">
            {isLoggedIn ? "Level 6 Adept Engineer" : "Level X Unkown..."}
          </h1>
        </div>
        <div className="flex justify-end items-center">
          <GoogleLogin />
        </div>
      </header>
      <div className="grid grid-cols-3 gap-2 justify-centre justify-items-center mb-8">
        <div>
          <Button text="Talent Tree" onClick={() => alert("clicked")} />
        </div>
        <div>
          <Button text="Select Title" onClick={() => alert("clicked")} />
        </div>
        <div>
          <Button
            text="Completed Quests"
            onClick={() => alert("clicked")}
          />
        </div>
      </div>

      {/* Body: Stats Section */}
      {/* If not logged in, we apply opacity and disable pointer events */}
      <div
        className={`grid gap-8 ${
          !isLoggedIn ? "opacity-50 pointer-events-none" : ""
        }`}
      >
        <BranchBox
          text="Strength"
          onClick={handleStatClick}
          icon="icons/weight-lifting-up.png"
        />
        <BranchBox
          text="Knowledge"
          onClick={handleStatClick}
          icon="icons/book-aura.png"
        />
        <BranchBox
          text="Health"
          onClick={handleStatClick}
          icon="icons/health-potion.png"
        />
      </div>
    </div>
  );
};

export default Home;
