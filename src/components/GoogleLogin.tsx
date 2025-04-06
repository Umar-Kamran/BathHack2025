// GoogleLogin.tsx
import React from "react";
import { GoogleAuthProvider, signInWithPopup, signOut, UserCredential } from "firebase/auth";
import { auth } from "../lib/firebase";
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";
import { useAuthState } from "react-firebase-hooks/auth";

const GoogleLogin: React.FC = () => {
    const [user] = useAuthState(auth);
    const navigate = useNavigate();

    const handleSignInOut = async (): Promise<void> => {
        if (!user) {
            const provider = new GoogleAuthProvider();
            try {
                const result: UserCredential = await signInWithPopup(auth, provider);
                console.log("User signed in:", result.user);
                toast.success("Logged in successfully!", {
                    position: "top-center",
                });
                navigate("/");
            } catch (error: any) {
                console.error("Error during Google sign in:", error.message);
                toast.error(error.message, {
                    position: "bottom-center",
                });
            }
        } else {
            try {
                await signOut(auth);
                console.log("User signed out");
                toast.success("Logged out successfully!", {
                    position: "top-center",
                });
                navigate("/");
            } catch (error: any) {
                console.error("Error during sign out:", error.message);
                toast.error(error.message, {
                    position: "bottom-center",
                });
            }
        }
    };

    const classname = user
        ? "bg-[var(--color-secondary)] hover:bg-[#4bba86] text-[var(--color-primary)] font-bold py-2 px-4 rounded duration-100"
        : "bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded duration-100";

    return (
        <button onClick={handleSignInOut} className={classname}>
            {user ? "Log out" : "Sign in with Google"}
        </button>
    );
};

export default GoogleLogin;