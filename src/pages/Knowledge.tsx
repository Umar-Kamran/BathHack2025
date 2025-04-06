import React, { useEffect, useState } from "react";
import ChatModal from "../components/chatModel";
import {
  getFirestore,
  collection,
  query,
  where,
  getDocs,
  updateDoc,
  doc,
  increment,
  getDoc,
} from "firebase/firestore";
import { auth } from "../lib/firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";
import Button from "../components/HomeButton"; // Reuse for the Back button

type Quest = {
  questId: string;
  taskTitle: string;
  duration: number;
  xpPoints: number;
  tags: string[];
  status: string;
};

const EXP_THRESHOLD = 1000; // required XP for leveling up

const Knowledge: React.FC = () => {
  const [user] = useAuthState(auth);
  const branch = "knowledge";
  const [quests, setQuests] = useState<Quest[]>([]);
  const [completingQuests, setCompletingQuests] = useState<string[]>([]);
  const db = getFirestore();
  const navigate = useNavigate();
  const [showChat, setShowChat] = useState(false);

    const onChatClick = () => {
        setShowChat(!showChat);
    };

  useEffect(() => {
    if (!user) return;

    const fetchQuests = async () => {
      try {
        // Reference: /users/{user.uid}/branches/adventure/quests
        const questsRef = collection(
          db,
          "users",
          user.uid,
          "branches",
          branch, // Change to "strength" if needed.
          "quests"
        );
        // Query only active quests
        const questsQuery = query(questsRef, where("status", "==", "active"));
        const querySnapshot = await getDocs(questsQuery);
        const questList: Quest[] = [];
        console.log("Fetched quests:", querySnapshot.docs);
        querySnapshot.forEach((docSnap) => {
          questList.push({
            questId: docSnap.id,
            ...(docSnap.data() as Omit<Quest, "questId">),
          });
        });
        setQuests(questList);
      } catch (error) {
        console.error("Error fetching quests: ", error);
      }
    };

    fetchQuests();
  }, [user, db]);

  const handleComplete = async (questId: string) => {
    if (!user) return;
    try {
      // Update the quest's status in Firestore
      const questDocRef = doc(
        db,
        "users",
        user.uid,
        "branches",
        branch,
        "quests",
        questId
      );
      await updateDoc(questDocRef, { status: "completed" });
      console.log("Quest completed:", questId);

      // Find the completed quest to add its xpPoints to the user
      const completedQuest = quests.find((q) => q.questId === questId);
      console.log("Updating quest:", {     path: `users/${user.uid}/branches/${branch}/quests/${questId}`,     quest: completedQuest,   });
      if (completedQuest) {
        const userDocRef = doc(db, "users", user.uid);
        // Increment the user's currentExperience by the quest's xpPoints
        await updateDoc(userDocRef, { currentExperience: increment(completedQuest.xpPoints) });
        
        // Check if the user's XP meets or exceeds the threshold
        const userDocSnap = await getDoc(userDocRef);
        const userData = userDocSnap.data();
        if (userData && userData.currentExperience >= EXP_THRESHOLD) {
          // Level up the user and show a toast notification.
          await updateDoc(userDocRef, { userLevel: increment(1) });
          toast.success("Level Up!");
          const remainingXP = userData.currentExperience - EXP_THRESHOLD;
            await updateDoc(userDocRef, { currentExperience: remainingXP });
        }
      }

      // Trigger the slide-away animation
      setCompletingQuests((prev) => [...prev, questId]);
      setTimeout(() => {
        setQuests((current) => current.filter((q) => q.questId !== questId));
        setCompletingQuests((prev) => prev.filter((id) => id !== questId));
      }, 300); // 300ms delay (match with your transition duration)
    } catch (error) {
      console.error("Error completing quest:", error);
    }
  };

  return (
    <div className="min-h-screen bg-[url('/icons/bg.png')] bg-cover bg-center text-white p-4">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <div className="mb-4 grid grid-cols-5 gap-4">
          <div className="col-span-3 shadow-xl shadow-black">
            <Button text="Back" onClick={() => navigate(-1)} />
          </div>
          <div className="col-span-2 flex items-center justify-left bg-[var(--color-secondary)] hover:text-white duration-200 text-[var(--color-primary)] text-3xl rounded py-3 px-20 cursor-pointer shadow-xl shadow-black"
            onClick={onChatClick}>
            <img
              src={"icons/chat-bubble.png"}
              alt="icon"
              className="w-9 h-9 mr-2"
            />
            <span>Chat</span>
          </div>
        </div>
        <h1 className="text-4xl font-bold mb-4 text-center text-[var(--color-secondary)]">
          Active Knowledge Quests:
        </h1>
        {quests.length === 0 ? (
          <div className="text-xl text-[var(--color-tertiary)] text-center">No active quests found.</div>
        ) : (
          <div className="w-full flex flex-col space-y-4">
            {quests.map((quest) => {
              // Add slide-away effect if quest is completing
              const cardClasses = completingQuests.includes(quest.questId)
                ? "rounded shadow p-4 bg-[var(--color-secondary)] text-[var(--color-primary)] transition duration-300 transform translate-x-full opacity-0"
                : "rounded shadow hover:bg-[#4bba86] p-4 bg-[var(--color-secondary)] text-[var(--color-primary)] hover:shadow-xl transition duration-200 relative";
              return (
                <div key={quest.questId} className={cardClasses}>
                  <h2 className="text-2xl font-semibold">{quest.taskTitle}</h2>
                  <div className="grid grid-cols-3 gap-4 mt-2">
                    <div>XP Points: {quest.xpPoints}</div>
                    <div>Duration: {quest.duration} minutes</div>
                    <div className="flex items-center space-x-2">
                      <span className="font-semibold">Tags:</span>
                      {quest.tags.map((tag, idx) => (
                        <span
                          key={idx}
                          className="font-normal bg-[var(--color-primary)] text-[var(--color-secondary)] px-2 py-0.5 rounded-md"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                  {/* Checkbox for marking quest as complete */}
                  <input
                    type="checkbox"
                    style={{ accentColor: "var(--color-primary)"}}
                    className="absolute top-2 right-2 w-6 h-6 cursor-pointer text-[var(--color-secondary)] rounded-full shadow-lg"
                    onChange={() => handleComplete(quest.questId)}
                  />
                </div>
              );
            })}
          </div>
        )}

        {/* chat component */}
        {showChat && <ChatModal onClose={() => setShowChat(false)} branch={branch}/>}
      </div>
    </div>
  );
};

export default Knowledge;