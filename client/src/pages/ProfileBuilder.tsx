import { FormEvent, useState } from "react";
import { SeekerProfile, useAppContext } from "../context/AppContext";
import { createProfile } from "../api/core";

const tagSuggestions = ["inventory", "transport", "customer", "navigation", "electric"];

export const ProfileBuilder = () => {
  const { profile, setProfile, isProfileSaved, setIsProfileSaved } = useAppContext();
  const [localProfile, setLocalProfile] = useState<SeekerProfile>(profile);
  const [step, setStep] = useState(0);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const prompts = [
    {
      label: "Do you have past experience?",
      key: "experienceYears",
      placeholder: "Years of experience"
    },
    {
      label: "What interests motivate you?",
      key: "interests",
      placeholder: "Community service, field work"
    }
  ];


  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setIsSubmitting(true);
    setMessage(null);
    createProfile(localProfile)
      .then((saved) => {
        setProfile(saved);
        setLocalProfile(saved);
        setIsProfileSaved(true);
        setMessage("Profile saved to JobsUPI cloud");
      })
      .catch(() => {
        setMessage("Could not save profile. Please try again.");
      })
      .finally(() => setIsSubmitting(false));
  };

  return (
    <section className="space-y-8">
      <div>
        <p className="text-sm uppercase tracking-wide text-brand-600">Profile Guide</p>
        <h1 className="text-3xl font-semibold text-slate-900">Tell us about yourself</h1>
        <p className="text-slate-500">A simple conversational form to capture your strengths.</p>
      </div>
      <form onSubmit={handleSubmit} className="grid gap-6 rounded-3xl bg-white p-6 shadow-lg">
        <div className="grid gap-2">
          <label className="text-sm font-medium">Name</label>
          <input
            className="rounded-xl border border-slate-200 p-3"
            value={localProfile.name ?? ""}
            onChange={(e) => setLocalProfile({ ...localProfile, name: e.target.value })}
            placeholder="Asha Kumari"
          />
        </div>
        <div className="grid gap-2">
          <label className="text-sm font-medium">Location</label>
          <input
            className="rounded-xl border border-slate-200 p-3"
            value={localProfile.location ?? ""}
            onChange={(e) => setLocalProfile({ ...localProfile, location: e.target.value })}
            placeholder="Kolkata"
          />
        </div>
        <div className="grid gap-2">
          <label className="text-sm font-medium">Skills (comma separated)</label>
          <input
            className="rounded-xl border border-slate-200 p-3"
            value={localProfile.skills.join(", ")}
            onChange={(e) => setLocalProfile({ ...localProfile, skills: e.target.value.split(/,\s*/) })}
          />
          <div className="text-xs text-slate-500">
            Suggestions: {tagSuggestions.join(", ")}
          </div>
        </div>
        {message && <p className="text-sm text-brand-600">{message}</p>}
        <button disabled={isSubmitting} className="rounded-2xl bg-brand-600 px-6 py-3 text-sm font-semibold text-white shadow-lg shadow-brand-600/30 disabled:opacity-60">
          {isSubmitting ? 'Saving...' : 'Save profile'}
        </button>
      </form>
    </section>
  );
};
