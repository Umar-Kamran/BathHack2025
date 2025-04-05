import Button from "../components/HomeButton";
import GoogleLogin from "./GoogleLogin";
import BranchBox from "../components/BranchBox"; // Import BranchBox
import { auth } from "../lib/firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { useEffect, useState } from "react";
import { doc, getDoc, getFirestore } from "firebase/firestore";

type PlayerData = {
  displayName: string;
  userLevel: number;
  titles: string[];
  currentExperience: number;
};

const Home: React.FC = () => {
  const [user] = useAuthState(auth);
  const isLoggedIn = !!user;
  const [playerData, setPlayerData] = useState<PlayerData | null>(null);
  const db = getFirestore();

  const expNeeded = 1000;
  const expPercent =
    playerData && playerData.currentExperience
      ? Math.min((playerData.currentExperience / expNeeded) * 100, 100)
      : 0;

  useEffect(() => {
    if (!user) {
      console.error("Waiting for user...");
      return;
    }
    const fetchPlayerData = async () => {
      console.log("Fetching player data for user:", user.uid);
      try {
        const docRef = doc(db, "users", user.uid);
        const docSnap = await getDoc(docRef);
        if (docSnap.exists()) {
          setPlayerData(docSnap.data() as PlayerData);
        } else {
          console.error("No player data found.");
        }
      } catch (error) {
        console.error("Error fetching player data:", error);
      }
    };
    fetchPlayerData();
  }, [user, db]);

  // New effect to clear player data when user signs out
  useEffect(() => {
    if (!user) {
      setPlayerData(null);
    }
  }, [user]);

  const handleStatClick = () => {
    if (!isLoggedIn) {
      alert("Login to continue");
    } else {
      alert("do some stuff");
    }
  };

  return (
    // min-h-screen bg-[var(--color-primary)] justify-center text-white p-4
    <div className="min-h-screen bg-[url('/icons/bg.png')] bg-cover bg-center justify-center text-white p-4">
      <header className="grid grid-cols-5 items-center mb-8">
        <div className="justify-start items-center">
          <img src={"icons/raw.png"} alt="icon" className="w-25 h-25 mx-10" />
        </div>
        <div className="col-span-3 p-6 mx-6">
          <div className="text-center">
            <h1 className="text-6xl font-bold text-[var(--color-secondary)]">
              {isLoggedIn && playerData
                ? `Level ${playerData.userLevel} ${playerData.titles[0]}`
                : "Level X Unknown..."}
            </h1>
            <div className="mt-4 flex justify-center">
              {isLoggedIn && playerData ? (
                <div className="w-full max-w-lg bg-gray-700 rounded-full h-4">
                  <div
                    className="bg-secondary h-4 rounded-full"
                    style={{ width: `${expPercent}%` }}
                  ></div>
                </div>
              ) : (
                <div className="w-full max-w-lg bg-gray-700 rounded-full h-4">
                  <div
                    className="bg-gray-500 h-4 rounded-full"
                    style={{ width: `0%` }}
                  ></div>
                </div>
              )}
            </div>
          </div>
        </div>
        <div className="flex justify-center items-center">
          <GoogleLogin />
        </div>
      </header>
      <div
        className={`grid grid-cols-3 gap-2 justify-center justify-items-center mb-8 ${
          isLoggedIn ? "" : "opacity-50 pointer-events-none"
        }`}
      >
        <div>
          <Button text="Talent Tree" onClick={() => alert("clicked")} />
        </div>
        <div>
          <Button text="Select Title" onClick={() => alert("clicked")} />
        </div>
        <div>
          <Button text="Completed Quests" onClick={() => alert("clicked")} />
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