import { useState } from "react";
import api from "../../services/api";
import { ShieldAlert, Clipboard, Sparkles } from "lucide-react";
import toast from "react-hot-toast";

function ScamDetector() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeScam = async () => {
    if (!text.trim()) return;

    try {
      setLoading(true);

      const response = await api.post("/scam/analyze-text", {
        text,
      });

      toast.success("Analysis completed");
    } catch (error) {
      console.error(error);
      toast.error("Unable to analyze message.");
    } finally {
      setLoading(false);
    }
  };

  const sampleMessage = () => {
    setText(
      "Dear Customer, Your SBI account has been blocked. Verify your account immediately by clicking https://fake-bank-login.com or your account will be permanently suspended."
    );
  };

  const copyResult = () => {
    if (!result) return;

    navigator.clipboard.writeText(
      JSON.stringify(result, null, 2)
    );
  };

  const getRiskColor = (score) => {
    if (score >= 80) return "bg-red-500";
    if (score >= 50) return "bg-yellow-500";
    return "bg-green-500";
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">

      <div className="max-w-5xl mx-auto">

        <h1 className="text-4xl font-bold flex items-center gap-3 mb-2">
          <ShieldAlert className="text-red-400" />
          Scam Detector
        </h1>

        <p className="text-slate-400 mb-8">
          Paste any suspicious SMS, email, or WhatsApp message for AI analysis.
        </p>

        <textarea
          rows={8}
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste suspicious message..."
          className="w-full bg-slate-800 rounded-xl p-5 outline-none border border-slate-700"
        />

        <div className="flex gap-4 mt-5">

          <button
            onClick={analyzeScam}
            disabled={loading}
            className="bg-cyan-500 text-black px-6 py-3 rounded-xl font-semibold hover:bg-cyan-400"
          >
            {loading ? "Analyzing..." : "Analyze"}
          </button>

          <button
            onClick={sampleMessage}
            className="bg-slate-700 px-6 py-3 rounded-xl hover:bg-slate-600"
          >
            Sample Message
          </button>

        </div>

        {result && (
          <div className="mt-10 space-y-5">

            <div className="flex justify-between items-center">

              <span
                className={`px-5 py-2 rounded-full font-bold ${getRiskColor(
                  result.risk_score
                )}`}
              >
                Risk Score : {result.risk_score}%
              </span>

              <button
                onClick={copyResult}
                className="flex items-center gap-2 bg-slate-800 px-4 py-2 rounded-lg"
              >
                <Clipboard size={18} />
                Copy
              </button>

            </div>

            <div className="bg-slate-800 rounded-xl p-5">
              <h2 className="font-bold text-cyan-400 mb-2">
                Fraud Type
              </h2>

              {result.fraud_type}
            </div>

            <div className="bg-slate-800 rounded-xl p-5">
              <h2 className="font-bold text-cyan-400 mb-2">
                Explanation
              </h2>

              {result.explanation}
            </div>

            <div className="bg-slate-800 rounded-xl p-5">
              <h2 className="font-bold text-cyan-400 mb-2 flex items-center gap-2">
                <Sparkles size={18} />
                Recommendation
              </h2>

              {result.recommendation}
            </div>

          </div>
        )}

      </div>

    </div>
  );
}

export default ScamDetector;