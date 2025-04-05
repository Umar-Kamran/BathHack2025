// GoogleLogin.tsx
import React from "react";
import { GoogleAuthProvider, signInWithPopup, UserCredential } from "firebase/auth";
import { auth } from "../lib/firebase"; // Adjust the import path as necessary
import { toast } from "react-toastify";

const GoogleLogin: React.FC = () => {
  const handleGoogleSignIn = async (): Promise<void> => {
    const provider = new GoogleAuthProvider();
    try {
      const result: UserCredential = await signInWithPopup(auth, provider);
      console.log(result);
      toast.success("Logged in successfully!", {
        position: "top-center",
      });
      // Optionally, redirect or update your app's state here.
      window.location.href = "/profile";
    } catch (error: any) {
      console.error("Error during Google sign in:", error.message);
      toast.error(error.message, {
        position: "bottom-center",
      });
    }
  };

  return (
    <button
      onClick={handleGoogleSignIn}
      className="bg-blue-500 hover:bg-blue-600 text-white font-bold py-2 px-4 rounded"
    >
      Sign in with Google
    </button>
  );
};

export default GoogleLogin;