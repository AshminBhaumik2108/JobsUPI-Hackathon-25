import { Request, Response } from "express";
import { JobPosting } from "../schemas/JobPosting";
import { asyncHandler } from "../utils/asyncHandler";

export const listJobs = asyncHandler(async (req, res) => {
  const { location, roleId, salaryMin, salaryMax } = req.query;
  const filter: any = {};
  if (location) filter.location = location;
  if (roleId) filter.role = roleId;
  if (salaryMin || salaryMax) {
    filter.salaryMin = { $gte: Number(salaryMin) || 0 };
    filter.salaryMax = { $lte: Number(salaryMax) || Infinity };
  }
  const jobs = await JobPosting.find(filter).populate("role");
  res.json(jobs);
});

export const createJob = asyncHandler(async (req, res) => {
  const job = await JobPosting.create(req.body);
  res.status(201).json(job);
});

export const updateJob = asyncHandler(async (req, res) => {
  const job = await JobPosting.findByIdAndUpdate(req.params.id, req.body, { new: true });
  res.json(job);
});

export const deleteJob = asyncHandler(async (req, res) => {
  await JobPosting.findByIdAndDelete(req.params.id);
  res.status(204).send();
});
