import { useState } from "react";
import api from "../../services/api";
import toast from "react-hot-toast";
import {
  Banknote,
  Upload,
  ShieldCheck,
  ShieldAlert,
} from "lucide-react";

function CurrencyDetector() {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleImage = (e) => {
    const file = e.target.files[0];

    if (!file) return;

    setImage(file);
    setPreview(URL.createObjectURL(file));
    setResult(null);
  };

  const analyzeCurrency = async () => {
    if (!image) {
      toast.error("Please upload an image first.");
      return;
    }

    const formData = new FormData();
    formData.append("file", image);

    try {
      setLoading(true);

      const response = await api.post(
        "/currency/analyze",
        formData
      );

      console.log("Currency API Response:", response.data);

      setResult(response.data);

      toast.success("Currency analyzed successfully");
    } catch (err) {
      console.error(err);
      toast.error("Unable to analyze image.");
    } finally {
      setLoading(false);
    }
  };

  const isGenuine =
    result?.status?.toLowerCase().includes("genuine") ||
    result?.status?.toLowerCase().includes("authentic");

  const confidenceMap = {
    Low: 30,
    Medium: 60,
    High: 90,
  };

  const confidence =
    confidenceMap[result?.confidence] ??
    Number(result?.confidence?.toString().replace("%", "")) ??
    0;

  return (
    <div className="min-h-screen bg-slate-950 text-white p-8">
      <div className="max-w-5xl mx-auto">

        <h1 className="text-4xl font-bold flex items-center gap-3 mb-2">
          <Banknote className="text-green-400" />
          Currency Detector
        </h1>

        <p className="text-slate-400 mb-8">
          Upload a currency note and let AI inspect it.
        </p>

        <label className="border-2 border-dashed border-slate-700 rounded-xl h-72 flex flex-col justify-center items-center cursor-pointer hover:border-cyan-400 transition">

          {preview ? (
            <img
              src={preview}
              alt="preview"
              className="h-full object-contain rounded-xl"
            />
          ) : (
            <>
              <Upload size={50} className="mb-3 text-cyan-400" />
              <p>Click to Upload</p>
            </>
          )}

          <input
            type="file"
            hidden
            accept="image/*"
            onChange={handleImage}
          />
        </label>

        <button
          onClick={analyzeCurrency}
          disabled={loading}
          className="mt-6 bg-cyan-500 text-black font-bold px-8 py-3 rounded-xl hover:bg-cyan-400 disabled:opacity-60"
        >
          {loading ? "Analyzing..." : "Analyze Currency"}
        </button>

        {result && (
          <div className="mt-10 space-y-6">

            {/* Status */}

            <div
              className={`rounded-xl p-5 ${
                isGenuine ? "bg-green-900" : "bg-red-900"
              }`}
            >
              <div className="flex items-center gap-3">

                {isGenuine ? (
                  <ShieldCheck className="text-green-300" />
                ) : (
                  <ShieldAlert className="text-red-300" />
                )}

                <h2 className="text-2xl font-bold">
                  {result.status}
                </h2>

              </div>
            </div>

            {/* Confidence */}

            <div className="bg-slate-800 rounded-xl p-5">

              <h3 className="font-bold mb-3">
                Confidence
              </h3>

              <div className="w-full bg-slate-700 rounded-full h-4 overflow-hidden">

                <div
                  className="bg-cyan-400 h-4 rounded-full transition-all duration-700"
                  style={{
                    width: `${confidence}%`,
                  }}
                />

              </div>

              <p className="mt-3 font-semibold">
                {result.confidence}
              </p>

            </div>

            {/* Security Features */}

            <div className="bg-slate-800 rounded-xl p-5">

              <h3 className="font-bold text-cyan-400 mb-3">
                Security Features
              </h3>

              <p className="leading-7 whitespace-pre-line">
                {result.security_features}
              </p>

            </div>

            {/* Recommendation */}

            <div className="bg-slate-800 rounded-xl p-5">

              <h3 className="font-bold text-cyan-400 mb-3">
                Recommendation
              </h3>

              <p className="leading-7 whitespace-pre-line">
                {result.recommendation}
              </p>

            </div>

          </div>
        )}

      </div>
    </div>
  );
}

export default CurrencyDetector;