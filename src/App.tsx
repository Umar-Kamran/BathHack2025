import Home from './pages/Home'
import { ToastContainer } from 'react-toastify'
import 'react-toastify/dist/ReactToastify.css'
import GoogleLogin from './components/GoogleLogin'
import Strength from './pages/Strength'
import Maths from './pages/Maths'
import Physics from './pages/Physics'
import Chemistry from './pages/Chemistry'
import TalentTreePage from './pages/talentTree'
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Chat from './pages/chat'

function App() {

  return (
    <Router>
      <Routes>
        <Route path="/" element={<Chat />} />
        <Route path="/login" element={<GoogleLogin />} />
        <Route path="/strength" element={<Strength />} />
        <Route path="/talent-tree" element={<TalentTreePage />} />
        <Route path="/talent/t_maths" element={<Maths />} />
        <Route path="/talent/t_physics" element={<Physics />} />
        <Route path="/talent/t_chemistry" element={<Chemistry />} />
<<<<<<< HEAD
        <Route path="/umar" element={<Chat branch="umar" />} />
        <Route path="/neev" element={<Chat branch="neev" />} />
        <Route path="/aadhav" element={<Chat branch="aadhav" />} />
=======
>>>>>>> 297f8a927f217dc5dadd69fe17d706d76bb59df6
      </Routes>
      <ToastContainer />
    </Router>
  )
}

export default App
