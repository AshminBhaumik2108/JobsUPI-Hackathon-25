import { InsightCard } from "../components/cards/InsightCard";

export const Dashboard = () => {
  const stats = [
    { title: "Profile completeness", value: "82%", accent: "brand-600" },
    { title: "Recommended roles", value: 3, accent: "emerald-600" },
    { title: "Applications sent", value: 5, accent: "sky-600" }
  ];

  return (
    <section className="space-y-6">
      <div>
        <p className="text-sm uppercase tracking-wide text-brand-600">Progress snapshot</p>
        <h1 className="text-3xl font-semibold text-slate-900">Your dashboard</h1>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {stats.map((stat) => (
          <InsightCard key={stat.title} title={stat.title} value={stat.value} accent={stat.accent} />
        ))}
      </div>
      <div className="rounded-3xl border border-slate-100 bg-white p-6 shadow-sm">
        <h2 className="text-xl font-semibold">Next best action</h2>
        <p className="mt-2 text-sm text-slate-500">
          Take the customer empathy micro-course to strengthen your profile and unlock more customer-facing roles.
        </p>
      </div>
    </section>
  );
};
