import { Schema, model } from "mongoose";

const roadmapStepSchema = new Schema(
  {
    title: String,
    description: String,
    durationWeeks: Number,
    resources: [String],
  },
  { _id: false }
);

const roleTemplateSchema = new Schema(
  {
    title: { type: String, required: true, unique: true },
    description: String,
    skills: {
      mustHave: [String],
      niceToHave: [String],
    },
    personality: [String],
    environment: {
      mobility: String,
    },
    roadmap: [roadmapStepSchema],
  },
  { timestamps: true }
);

export const RoleTemplate = model("RoleTemplate", roleTemplateSchema);
