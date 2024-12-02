import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import LoginPage from "./components/LoginPage";
import UnitsPage from "./components/UnitsPage";
import TeacherDashboard from "./components/TeacherDashboard";
import KeepTrackPage from "./components/KeepTrackPage"; 
import TextPage from "./components/TextPage";
import ProfilePage from "./components/ProfilePage"
import QuizPage from "./components/QuizPage"; 
import PastQuizAttemptPage from "./components/PastQuizAttemptPage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/units" element={<UnitsPage />} />
        <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
        <Route path="/keep-track/" element={<KeepTrackPage />} />
        <Route path="/text/:textId" element={<TextPage />} /> 
        <Route path="/profile/" element={<ProfilePage />} />
        <Route path="/quiz" element={<QuizPage />} /> 
        <Route path="/quiz-attempts" element={<PastQuizAttemptPage />} /> 

      </Routes>
    </Router>
  );
}
export default App;
