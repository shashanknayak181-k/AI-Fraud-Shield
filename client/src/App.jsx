import { Routes, Route } from "react-router-dom";

import Dashboard from "./pages/Dashboard/Dashboard";
import ScamDetector from "./pages/ScamDetector/ScamDetector";
import CurrencyDetector from "./pages/CurrencyDetector/CurrencyDetector";
import Chatbot from "./pages/Chatbot/Chatbot";

import Navbar from "./components/layout/Navbar";
import Footer from "./components/layout/Footer";

function App() {
  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/scam-detector" element={<ScamDetector />} />
          <Route path="/currency-detector" element={<CurrencyDetector />} />
          <Route path="/chatbot" element={<Chatbot />} />
        </Routes>
      </main>

      <Footer />
    </div>
  );
}

export default App;