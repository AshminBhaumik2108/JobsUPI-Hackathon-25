import { Request, Response } from "express";
import { RoleTemplate } from "../schemas/RoleTemplate";
import { asyncHandler } from "../utils/asyncHandler";

export const listRoles = asyncHandler(async (req, res) => {
  const { mobility, skill } = req.query;
  const filter: any = {};
  if (mobility) filter["environment.mobility"] = mobility;
  if (skill) filter["skills.mustHave"] = skill;
  const roles = await RoleTemplate.find(filter);
  res.json(roles);
});

export const getRole = asyncHandler(async (req, res) => {
  const role = await RoleTemplate.findById(req.params.id);
  res.json(role);
});

export const createRole = asyncHandler(async (req, res) => {
  const role = await RoleTemplate.create(req.body);
  res.status(201).json(role);
});
