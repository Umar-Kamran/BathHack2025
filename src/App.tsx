import { useState } from 'react'
import Home from './pages/home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './pages/GoogleLogin'
import TalentTreePage from './pages/talentTree'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Chat from './pages/chat'
function App() {

  return (
    <div>
      <TalentTreePage />
    </div>
  );
}

export default App
