import { Schema, model } from "mongoose";

const userProfileSchema = new Schema(
  {
    name: { type: String },
    contact: { type: String },
    skills: [String],
    interests: [String],
    personality: [String],
    location: { type: String },
    experienceYears: { type: Number },
  },
  { timestamps: true }
);

export const UserProfile = model("UserProfile", userProfileSchema);
