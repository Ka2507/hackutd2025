/**
 * Main App Component
 */
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import ProjectDashboard from './pages/ProjectDashboard';
import Insights from './pages/Insights';
import Chat from './pages/Chat';
import './styles/index.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<ProjectDashboard />} />
        <Route path="/insights" element={<Insights />} />
        <Route path="/chat" element={<Chat />} />
      </Routes>
    </Router>
  );
}

export default App;

