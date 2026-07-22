import { NavLink } from "react-router-dom";
import { ShieldCheck } from "lucide-react";

function Navbar() {
  const linkStyle = ({ isActive }) =>
    `transition ${
      isActive
        ? "text-cyan-400 font-semibold"
        : "text-slate-300 hover:text-cyan-400"
    }`;

  return (
    <nav className="sticky top-0 z-50 bg-slate-900/90 backdrop-blur border-b border-slate-800">
      <div className="max-w-7xl mx-auto flex justify-between items-center px-8 py-4">

        <div className="flex items-center gap-3">
          <ShieldCheck size={32} className="text-cyan-400" />
          <span className="text-2xl font-bold text-white">
            AI Fraud Shield
          </span>
        </div>

        <div className="flex gap-8 text-sm">

          <NavLink to="/" className={linkStyle}>
            Dashboard
          </NavLink>

          <NavLink to="/scam-detector" className={linkStyle}>
            Scam Detector
          </NavLink>

          <NavLink to="/currency-detector" className={linkStyle}>
            Currency
          </NavLink>

          <NavLink to="/chatbot" className={linkStyle}>
            AI Assistant
          </NavLink>

        </div>

      </div>
    </nav>
  );
}

export default Navbar;