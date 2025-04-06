import Home from './pages/home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './components/GoogleLogin'
import Strength from './pages/Strength'
import Maths from './pages/Maths'
import Physics from './pages/Physics'
import Chemistry from './pages/Chemistry'
import TalentTreePage from './pages/talentTree'
import Health from './pages/Health'
import Knowledge from './pages/Knowledge'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import CompletedQuests from './pages/CompletedQuests'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<GoogleLogin />} />
        <Route path="/strength" element={<Strength />} />
        <Route path="/completed" element={<CompletedQuests />} />
        <Route path="/health" element={<Health />} />
        <Route path="/knowledge" element={<Knowledge />} />
        <Route path="/talent-tree" element={<TalentTreePage />} />
        <Route path="/talent/t_maths" element={<Maths />} />
        <Route path="/talent/t_physics" element={<Physics />} />
        <Route path="/talent/t_chemistry" element={<Chemistry />} />
      </Routes>
      <ToastContainer />
    </Router>
  )
}

export default App
