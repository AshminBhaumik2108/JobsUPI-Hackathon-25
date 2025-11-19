import { useQuery } from "@tanstack/react-query";
import { getJobs } from "../api/core";

export const JobsBoard = () => {
  const { data: jobs } = useQuery({
    queryKey: ["jobs"],
    queryFn: () => getJobs({ location: "Kolkata" })
  });

  return (
    <section className="space-y-6">
      <div>
        <p className="text-sm uppercase tracking-wide text-brand-600">Matched openings</p>
        <h1 className="text-3xl font-semibold text-slate-900">Opportunities tailored to you</h1>
      </div>
      <div className="grid gap-4">
        {jobs?.map((job: any) => (
          <div key={job._id} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm uppercase text-slate-400">{job.employer}</p>
                <h2 className="text-xl font-semibold">{job.role?.title ?? "Role"}</h2>
              </div>
              <span className="text-sm font-semibold text-brand-600">
                ₹{job.salaryMin?.toLocaleString()} - ₹{job.salaryMax?.toLocaleString()}
              </span>
            </div>
            <p className="mt-2 text-sm text-slate-500">{job.location}</p>
            <p className="mt-3 text-xs text-slate-400">Shift: {job.shift ?? "Flexible"}</p>
          </div>
        ))}
      </div>
    </section>
  );
};
