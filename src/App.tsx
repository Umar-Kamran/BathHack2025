import { useState } from 'react'
import Home from './pages/home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './components/GoogleLogin'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<GoogleLogin />} />
      </Routes>
      <ToastContainer />
    </Router>
  )
}

export default App
