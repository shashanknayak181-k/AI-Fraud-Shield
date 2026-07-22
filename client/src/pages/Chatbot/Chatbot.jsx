import { useState, useRef, useEffect } from "react";
import api from "../../services/api";
import { Bot, Send } from "lucide-react";
import toast from "react-hot-toast";

const suggestions = [
  "How do phishing emails work?",
  "What is a digital arrest scam?",
  "How do fake UPI screenshots work?",
  "What should I do after sharing my OTP?"
];

function Chatbot() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const bottomRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  const sendMessage = async (text = question) => {
    if (!text.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        sender: "user",
        text,
      },
    ]);

    setQuestion("");

    try {
      setLoading(true);

      const res = await api.post("/assistant/chat", {
        question: text,
      });

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: res.data.answer,
        },
      ]);
    } catch {
      toast.error("Unable to contact AI Assistant");

      setMessages((prev) => [
        ...prev,
        {
          sender: "ai",
          text: "Unable to contact AI.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white flex flex-col">

      <div className="bg-slate-900 p-6 border-b border-slate-700">

        <h1 className="text-3xl font-bold flex items-center gap-3">

          <Bot className="text-cyan-400" />

          AI Fraud Assistant

        </h1>

      </div>

      <div className="flex-1 overflow-y-auto p-6">

        {messages.length === 0 && (
          <div>

            <h2 className="text-xl mb-4">
              Try asking
            </h2>

            <div className="flex flex-wrap gap-3">

              {suggestions.map((s) => (
                <button
                  key={s}
                  onClick={() => sendMessage(s)}
                  className="bg-slate-800 hover:bg-slate-700 rounded-full px-4 py-2"
                >
                  {s}
                </button>
              ))}

            </div>

          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex mb-5 ${msg.sender === "user"
                ? "justify-end"
                : "justify-start"
              }`}
          >
            <div
              className={`max-w-[70%] rounded-2xl px-5 py-3 ${msg.sender === "user"
                  ? "bg-cyan-500 text-black"
                  : "bg-slate-800"
                }`}
            >
              {msg.text}
            </div>
          </div>
        ))}

        {loading && (
          <div className="bg-slate-800 inline-block rounded-xl px-5 py-3">
            AI is typing...
          </div>
        )}

        <div ref={bottomRef}></div>

      </div>

      <div className="border-t border-slate-700 p-5 flex gap-3">

        <input
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          onKeyDown={(e) =>
            e.key === "Enter" && sendMessage()
          }
          placeholder="Ask anything about cyber fraud..."
          className="flex-1 bg-slate-800 rounded-xl px-5 py-3 outline-none"
        />

        <button
          onClick={() => sendMessage()}
          disabled={loading}
          className="bg-cyan-500 text-black px-6 rounded-xl"
        >
          <Send />
        </button>

      </div>

    </div>
  );
}

export default Chatbot;