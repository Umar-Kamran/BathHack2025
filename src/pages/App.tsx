import Home from './pages/Home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './components/GoogleLogin'
import Strength from './pages/Strength'
import TalentTreePage from './pages/talentTree'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Chat from './pages/chat'
function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<GoogleLogin />} />
        <Route path="/strength" element={<Strength />} />
        <Route path="/talent-tree" element={<TalentTreePage />} />
      </Routes>
      <ToastContainer />
    </Router>
  )
}

export default App
