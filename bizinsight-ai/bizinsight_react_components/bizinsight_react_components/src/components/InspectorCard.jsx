export default function InspectorCard({ icon, title, children, className = "" }) {
  return (
    <div className={`detail-card ${className}`}>
      <div className="card-title">{icon}{title}</div>
      {children}
    </div>
  );
}
