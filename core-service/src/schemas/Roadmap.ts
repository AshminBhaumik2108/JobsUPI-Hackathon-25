import { Schema, model, Types } from "mongoose";

const roadmapSchema = new Schema(
  {
    role: { type: String, required: true },
    userProfile: { type: Types.ObjectId, ref: "UserProfile", required: true },
    steps: [
      {
        title: String,
        description: String,
        durationWeeks: Number,
        resources: [String],
      },
    ],
  },
  { timestamps: true }
);

export const Roadmap = model("Roadmap", roadmapSchema);
