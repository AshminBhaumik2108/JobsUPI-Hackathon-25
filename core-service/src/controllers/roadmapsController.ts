import { Request, Response } from "express";
import { Roadmap } from "../schemas/Roadmap";
import { asyncHandler } from "../utils/asyncHandler";


export const getRoadmapById = asyncHandler(async (req, res) => {
  const roadmap = await Roadmap.findById(req.params.id);
  if (!roadmap) {
    res.status(404).json({ message: "Roadmap not found" });
    return;
  }
  res.json(roadmap);
});

export const listRoadmaps = asyncHandler(async (req, res) => {
  const { roleId, userProfileId } = req.query as { roleId?: string; userProfileId?: string };
  const filter: Record<string, unknown> = {};
  if (roleId) {
    filter.role = roleId;
  }
  if (userProfileId) {
    filter.userProfile = userProfileId;
  }
  const roadmaps = await Roadmap.find(filter);
  res.json(roadmaps);
});

export const createRoadmap = asyncHandler(async (req, res) => {
  const roadmap = await Roadmap.create(req.body);
  res.status(201).json(roadmap);
});
