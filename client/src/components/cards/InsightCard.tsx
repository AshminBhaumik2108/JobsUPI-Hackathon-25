import { ReactNode } from "react";

export const InsightCard = ({ title, value, accent }: { title: string; value: ReactNode; accent: string }) => (
  <div className="rounded-2xl border border-slate-200 bg-white/70 p-5 shadow-sm backdrop-blur">
    <p className="text-xs uppercase tracking-wide text-slate-400">{title}</p>
    <p className={`mt-2 text-2xl font-semibold text-${accent}`}>{value}</p>
  </div>
);
