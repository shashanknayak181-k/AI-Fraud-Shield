function FeatureCard({ title, description, icon, onClick }) {
  return (
    <div
      onClick={onClick}
      className="cursor-pointer rounded-2xl bg-slate-800 border border-slate-700 p-8 transition-all duration-300 hover:-translate-y-2 hover:border-cyan-400 hover:shadow-2xl hover:shadow-cyan-500/20"
    >
      <div className="text-cyan-400 mb-5">
        {icon}
      </div>

      <h2 className="text-2xl font-bold mb-3">
        {title}
      </h2>

      <p className="text-slate-400">
        {description}
      </p>
    </div>
  );
}

export default FeatureCard;