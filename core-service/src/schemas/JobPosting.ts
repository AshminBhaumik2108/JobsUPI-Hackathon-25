import { Schema, model, Types } from "mongoose";

const jobPostingSchema = new Schema(
  {
    role: { type: Types.ObjectId, ref: "RoleTemplate", required: true },
    employer: String,
    location: String,
    salaryMin: Number,
    salaryMax: Number,
    shift: String,
    status: { type: String, default: "open" },
  },
  { timestamps: true }
);

jobPostingSchema.index({ role: 1, location: 1 });

export const JobPosting = model("JobPosting", jobPostingSchema);
