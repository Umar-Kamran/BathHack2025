import React, { useEffect, useState } from "react";
import {
  getFirestore,
  collection,
  getDocs,
  query,
  where,
} from "firebase/firestore";
import { auth } from "../lib/firebase";
import { useAuthState } from "react-firebase-hooks/auth";
import { useNavigate } from "react-router-dom";
import Button from "../components/HomeButton";
import { toast } from "react-toastify";

type Quest = {
  questId: string;
  taskTitle: string;
  duration: number;
  xpPoints: number;
  tags: string[];
  status: string;
  branch: string;
};

const CompletedQuests: React.FC = () => {
  const [user] = useAuthState(auth);
  const [quests, setQuests] = useState<Quest[]>([]);
  const db = getFirestore();
  const navigate = useNavigate();

  useEffect(() => {
    if (!user) return;

    // Loop through all branches and aggregate completed quests.
    const fetchCompletedQuests = async () => {
      try {
        const questList: Quest[] = [];
        // Get all branches under the current user
        const branchesRef = collection(db, "users", user.uid, "branches");
        const branchesSnap = await getDocs(branchesRef);

        // Loop through each branch
        for (const branchDoc of branchesSnap.docs) {
          const branchId = branchDoc.id;
          const questsRef = collection(db, "users", user.uid, "branches", branchId, "quests");
          // Query only completed quests for this branch
          const questsQuery = query(questsRef, where("status", "==", "completed"));
          const questsSnap = await getDocs(questsQuery);

          questsSnap.forEach((docSnap) => {
            questList.push({
              questId: docSnap.id,
              ...(docSnap.data() as Omit<Quest, "questId" | "branch">),
              branch: branchId,
            });
          });
        }
        console.log("Fetched completed quests (via branches):", questList.length);
        setQuests(questList);
      } catch (error) {
        console.error("Error fetching completed quests:", error);
        toast.error("Error fetching completed quests");
      }
    };

    fetchCompletedQuests();
  }, [user, db]);

  return (
    <div className="min-h-screen bg-[url('/icons/bg.png')] bg-cover bg-center text-white p-4">
      <div className="max-w-4xl mx-auto">
        {/* Back Button */}
        <div className="mb-4">
          <Button text="Back" onClick={() => navigate(-1)} />
        </div>
        <h1 className="text-4xl font-bold mb-4 text-center text-[var(--color-secondary)]">
          Completed Quests
        </h1>
        {quests.length === 0 ? (
          <div className="text-xl text-[var(--color-tertiary)] text-center">
            No completed quests found.
          </div>
        ) : (
          <div className="w-full flex flex-col space-y-4">
            {quests.map((quest) => (
              <div
                key={quest.questId}
                className="rounded shadow p-4 bg-[var(--color-secondary)] text-[var(--color-primary)] hover:shadow-xl transition duration-200 relative"
              >
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
                <div className="mt-2 text-sm italic">
                  Branch: {quest.branch}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default CompletedQuests;