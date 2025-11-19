import { useState } from "react";
import { useQuery, useQueryClient } from "@tanstack/react-query";
import { getRoadmaps, createRoadmap } from "../api/core";
import { fetchRoadmap } from "../api/agent";
import { useAppContext } from "../context/AppContext";

type AgentRoadmapResponse = {
  roadmap?: Array<{
    title: string;
    description: string;
    duration_weeks?: number;
    durationWeeks?: number;
    resources?: string[];
  }>;
  selected_role_id?: string;
  summary?: string;
};

export const RoadmapView = () => {
  const { profile, selectedRoleId } = useAppContext();
  const profileId = profile?._id;
  const queryClient = useQueryClient();
  const [isGenerating, setIsGenerating] = useState(false);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const { data: roadmaps, isFetching } = useQuery({
    queryKey: ["roadmaps", profileId],
    enabled: Boolean(profileId),
    queryFn: () => {
      if (!profileId) {
        return [];
      }
      return getRoadmaps({ userProfileId: profileId });
    }
  });

  const roadmap = roadmaps?.[0];

  const handleGenerateRoadmap = async () => {
    if (!profileId) {
      setStatusMessage("Fetch a seeker profile by ID first.");
      return;
    }

    setIsGenerating(true);
    setStatusMessage(null);

    try {
      const agentResponse: AgentRoadmapResponse = await fetchRoadmap({
        seeker_profile: profile,
        role_id: selectedRoleId
      });

      const normalizedSteps = (agentResponse.roadmap ?? []).map((step) => ({
        title: step.title,
        description: step.description,
        durationWeeks: step.durationWeeks ?? step.duration_weeks ?? 1,
        resources: step.resources ?? []
      }));

      if (!normalizedSteps.length) {
        throw new Error("Agent returned empty roadmap");
      }

      const roleForSave = selectedRoleId || agentResponse.selected_role_id;
      if (!roleForSave) {
        throw new Error("Missing role identifier for roadmap");
      }

      await createRoadmap({
        role: roleForSave,
        userProfile: profileId,
        steps: normalizedSteps
      });

      setStatusMessage("Roadmap saved to JobsUPI cloud.");
      await queryClient.invalidateQueries({ queryKey: ["roadmaps", profileId] });
    } catch (error) {
      console.error("Roadmap generation failed", error);
      setStatusMessage("Could not generate roadmap. Please try again.");
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <section className="space-y-6">
      <div className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
        <div>
          <p className="text-sm uppercase tracking-wide text-brand-600">Learning roadmap</p>
          <h1 className="text-3xl font-semibold text-slate-900">Steps to become job-ready</h1>
        </div>
        <button
          onClick={handleGenerateRoadmap}
          disabled={!profileId || isGenerating}
          className="rounded-2xl border border-brand-600 px-6 py-3 text-sm font-semibold text-brand-600 disabled:opacity-50"
        >
          {isGenerating ? "Generating..." : "Generate via AI agent"}
        </button>
      </div>

      {statusMessage && <p className="text-sm text-brand-600">{statusMessage}</p>}

      {!profileId ? (
        <p className="rounded-3xl border border-dashed border-slate-300 bg-white p-6 text-slate-500">
          Fetch a seeker profile by ID on the Roles screen, then return here to view the roadmap.
        </p>
      ) : !roadmap ? (
        <p className="rounded-3xl border border-dashed border-slate-300 bg-white p-6 text-slate-500">
          {isFetching ? "Loading roadmap..." : "No roadmap saved yet. Use the AI button above to draft one."}
        </p>
      ) : (
        <div className="space-y-4">
          {roadmap.steps.map((step: any, index: number) => (
            <div key={index} className="rounded-3xl border border-slate-200 bg-white p-5 shadow-sm">
              <div className="flex items-center gap-3">
                <span className="flex h-10 w-10 items-center justify-center rounded-full bg-brand-100 text-brand-600">
                  {index + 1}
                </span>
                <div>
                  <p className="text-sm uppercase text-slate-400">{step.durationWeeks ?? 1} weeks</p>
                  <h3 className="text-lg font-semibold">{step.title}</h3>
                </div>
              </div>
              <p className="mt-3 text-sm text-slate-600">{step.description}</p>
            </div>
          ))}
        </div>
      )}
    </section>
  );
};
