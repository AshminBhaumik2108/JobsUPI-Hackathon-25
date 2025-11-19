import { useState } from "react";
import { fetchRoleFit } from "../api/agent";
import { getRoles, getProfileById } from "../api/core";
import { useAppContext, SeekerProfile } from "../context/AppContext";
import { useQuery } from "@tanstack/react-query";

type RoleCandidate = {
  role_id: string;
  title: string;
  match_score: number;
  rationale: string;
};

export const RoleExplorer = () => {
  const { setProfile, setSelectedRoleId, roleInsight, setRoleInsight } = useAppContext();
  const [roleCandidates, setRoleCandidates] = useState<RoleCandidate[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [seekerId, setSeekerId] = useState<string>("");
  const [profile, setFetchedProfile] = useState<SeekerProfile | null>(null);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const rolesQuery = useQuery({
    queryKey: ["roles"],
    queryFn: () => getRoles()
  });

  const handleFetchProfile = async () => {
    try {
      setErrorMessage("");
      setRoleCandidates([]);
      setRoleInsight(undefined);
      const data = await getProfileById(seekerId.trim());
      setFetchedProfile(data);
      setProfile(data);
    } catch (error) {
      console.error("Failed to fetch profile", error);
      setFetchedProfile(null);
      setErrorMessage("Could not find profile for that ID.");
    }
  };

  const handleLLMRecommend = async () => {
    if (!profile) {
      setErrorMessage("Please fetch a profile using its Mongo ID first.");
      return;
    }
    setIsLoading(true);
    try {
      const response = await fetchRoleFit(profile);
      setRoleInsight(response.summary);
      setRoleCandidates(response.role_candidates);
      setSelectedRoleId(response.selected_role_id);
    } catch (error) {
      console.error("Role recommendation failed", error);
      setErrorMessage("Unable to fetch recommendations. Check logs.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-brand-600">Discover roles</p>
          <h1 className="text-3xl font-semibold text-slate-900">Best fit for your strengths</h1>
        </div>
      </div>

      <div className="flex flex-col gap-4 rounded-3xl bg-white p-6 shadow-sm md:flex-row md:items-end">
        <div className="flex-1">
          <label className="text-sm font-medium text-slate-600">Enter Seeker Mongo ID</label>
          <input
            value={seekerId}
            onChange={(e) => setSeekerId(e.target.value)}
            placeholder="665cabc1234..."
            className="mt-2 w-full rounded-2xl border border-slate-200 px-4 py-3"
          />
        </div>
        <button onClick={handleFetchProfile} className="rounded-2xl bg-brand-600 px-6 py-3 text-white">
          Fetch profile
        </button>
        <button
          onClick={handleLLMRecommend}
          disabled={isLoading}
          className="rounded-2xl border border-brand-600 px-6 py-3 text-brand-600 disabled:opacity-50"
        >
          {isLoading ? "Fetching..." : "Ask AI to recommend"}
        </button>
      </div>

      {errorMessage && <p className="text-sm text-red-600">{errorMessage}</p>}

      {profile && (
        <div className="rounded-3xl border border-slate-100 bg-slate-50 p-6">
          <p className="text-sm uppercase tracking-wide text-slate-500">Active seeker</p>
          <h3 className="text-xl font-semibold text-slate-900">{profile.name || "Unnamed seeker"}</h3>
          <p className="text-sm text-slate-500">{profile.location}</p>
          <div className="mt-3 flex flex-wrap gap-2 text-xs">
            {profile.skills.map((skill) => (
              <span key={skill} className="rounded-full bg-brand-50 px-3 py-1 text-brand-600">
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {roleCandidates.length > 0 && (
        <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-6 text-emerald-900">
          <p className="text-sm font-medium">AI Insight</p>
          <p className="text-lg">{roleInsight}</p>
        </div>
      )}

      {roleCandidates.length > 0 && (
        <div className="grid gap-4 md:grid-cols-2">
          {roleCandidates.map((candidate) => (
            <article key={candidate.role_id} className="rounded-3xl border border-brand-100 bg-white p-5 shadow-sm">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm uppercase text-slate-400">Gemini recommendation</p>
                  <h2 className="text-xl font-semibold">{candidate.title}</h2>
                </div>
                <span className="text-sm font-semibold text-brand-600">
                  {(candidate.match_score * 100).toFixed(0)}% fit
                </span>
              </div>
              <p className="mt-3 text-sm text-slate-500">{candidate.rationale}</p>
            </article>
          ))}
        </div>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        {rolesQuery.data?.map((role: any) => (
          <article key={role._id} className="rounded-3xl border border-slate-100 bg-white p-5 shadow-sm">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">{role.title}</h2>
              <span className="rounded-full bg-slate-100 px-4 py-1 text-xs uppercase text-slate-500">
                Mobility: {role.environment?.mobility ?? "flex"}
              </span>
            </div>
            <p className="mt-3 text-sm text-slate-500">{role.description}</p>
            <div className="mt-4 flex flex-wrap gap-2 text-xs">
              {role.skills?.mustHave?.map((skill: string) => (
                <span key={skill} className="rounded-full bg-brand-50 px-3 py-1 text-brand-600">
                  {skill}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </section>
  );
};
