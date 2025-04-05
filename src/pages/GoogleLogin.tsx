// GoogleLogin.tsx
import React, { useState } from "react";
import { GoogleAuthProvider, signInWithPopup, signOut, UserCredential } from "firebase/auth";
import { auth } from "../lib/firebase"; // Adjust the import path as necessary
import { toast } from "react-toastify";
import { useNavigate } from "react-router-dom";

const GoogleLogin: React.FC = () => {
    const [loggedIn, setLoggedIn] = useState(false);
    const navigate = useNavigate();

    const handleSignInOut = async (): Promise<void> => {
        if (!loggedIn) {
            const provider = new GoogleAuthProvider();
            try {
                const result: UserCredential = await signInWithPopup(auth, provider);
                console.log(result);
                toast.success("Logged in successfully!", {
                    position: "top-center",
                });
                setLoggedIn(true);
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
                toast.success("Logged out successfully!", {
                    position: "top-center",
                });
                setLoggedIn(false);
                navigate("/");
            } catch (error: any) {
                console.error("Error during sign out:", error.message);
                toast.error(error.message, {
                    position: "bottom-center",
                });
            }
        }
    };

    const classname = loggedIn
        ? "bg-green-500 hover:bg-green-600 text-white font-bold py-2 px-4 rounded duration-100"
        : "bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded duration-100";

    return (
        <button
            onClick={handleSignInOut}
            className={classname}
        >
            {loggedIn ? "Log out" : "Sign in with Google"}
        </button>
    );
};

export default GoogleLogin;