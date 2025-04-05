import { useState } from 'react'
import Home from './pages/home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './pages/GoogleLogin'
import Chat from "./pages/chat"; 
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {

  return (
    <div>
    <Chat />
  </div>
  )
}

export default App
