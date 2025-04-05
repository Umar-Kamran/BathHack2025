import { useState } from 'react'
import './App.css'
import Home from './pages/home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './pages/GoogleLogin'

function App() {

  return (
    // <>
    //   <div className="justify-center">
    //   <Home />
    //   </div>
    // </>
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      <h1 className="text-3xl font-bold mb-4">My App</h1>
      <GoogleLogin />
      <ToastContainer />
    </div>
  )
}

export default App
