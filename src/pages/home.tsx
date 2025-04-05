import Button from "../components/HomeButton";
import GoogleLogin from "../components/GoogleLogin";
import BranchBox from "../components/BranchBox"; // Import BranchBox
import { auth } from "../lib/firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { useEffect, useState } from "react";
import { doc, getDoc, getFirestore } from "firebase/firestore";
import TitleSelect from "../components/TitleSelect"; 
import { useNavigate } from "react-router-dom";

type PlayerData = {
  displayName: string;
  userLevel: number;
  titles: string[];
  currentExperience: number;
};

const Home: React.FC = () => {
  const navigate = useNavigate();
  const [user] = useAuthState(auth);
  const isLoggedIn = !!user;
  const [playerData, setPlayerData] = useState<PlayerData | null>(null);
  const [selectedTitle, setSelectedTitle] = useState<string>("");
  const [showModal, setShowModal] = useState(false);
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
          const data = docSnap.data() as PlayerData;
          setPlayerData(data);
          // Set the initial selected title from the player's list
          if (data.titles && data.titles.length > 0) {
            setSelectedTitle(data.titles[0]);
          }
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
                ? `Level ${playerData.userLevel} ${selectedTitle}`
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
        className={`grid grid-cols-1 sm:grid-cols-3 gap-4 justify-items-center opacity-90 mb-8 ${
          isLoggedIn ? "" : "opacity-50 pointer-events-none"
        }`}
      >
        <div className="w-full">
          <Button text="Talent Tree" onClick={() => alert("clicked")} />
        </div>
        <div className="w-full">
          <Button text="Select Title" onClick={() => setShowModal(true)} />
        </div>
        <div className="w-full">
          <Button text="Completed Quests" onClick={() => alert("clicked")} />
        </div>
      </div>
        {/* Branch boxes for stats */}
      <div
        className={`grid gap-8 opacity-90 ${
          !isLoggedIn ? "opacity-50 pointer-events-none" : ""
        }`}
      >
        <BranchBox
          text="Strength"
          onClick={() => navigate("/strength")}
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

        {/* Modal for title selection */}
        {showModal && playerData && (
            <TitleSelect
                titles={playerData.titles}
                onClose={() => setShowModal(false)}
                onTitleSelect={(title: string) => setSelectedTitle(title)}
            />
        )}
    </div>
  );
};

export default Home;