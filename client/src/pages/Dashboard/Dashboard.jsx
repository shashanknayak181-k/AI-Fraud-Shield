import { ShieldCheck, ScanSearch, Banknote, Bot } from "lucide-react";
import FeatureCard from "../../components/ui/FeatureCard";
import { useNavigate } from "react-router-dom";

function Dashboard() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-800 text-white">

      {/* Hero Section */}
      <div className="max-w-7xl mx-auto px-8 py-20 text-center">

        <div className="flex justify-center mb-6">
          <ShieldCheck size={70} className="text-cyan-400" />
        </div>

        <h1 className="text-6xl font-extrabold">
          AI Fraud Shield
        </h1>

        <p className="mt-6 text-xl text-slate-300 max-w-3xl mx-auto">
          AI-powered platform for detecting digital scams,
          counterfeit currency, and providing instant cyber safety guidance.
        </p>

      </div>

      {/* Features */}
      <div className="max-w-6xl mx-auto px-8 pb-20">

        <div className="grid md:grid-cols-3 gap-8">

          <FeatureCard
            title="Scam Detector"
            description="Analyze SMS, Emails and WhatsApp messages using Gemini AI."
            icon={<ScanSearch size={36} />}
            onClick={() => navigate("/scam-detector")}
          />

          <FeatureCard
            title="Currency Detector"
            description="Detect suspicious currency notes using AI Vision."
            icon={<Banknote size={36} />}
            onClick={() => navigate("/currency-detector")}
          />

          <FeatureCard
            title="AI Assistant"
            description="Ask fraud-related questions and receive expert guidance."
            icon={<Bot size={36} />}
            onClick={() => navigate("/chatbot")}
          />

        </div>

      </div>

    </div>
  );
}

export default Dashboard;