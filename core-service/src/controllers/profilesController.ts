import { UserProfile } from "../schemas/UserProfile";
import { asyncHandler } from "../utils/asyncHandler";

export const getProfileById = asyncHandler(async (req, res) => {
  const profile = await UserProfile.findById(req.params.id);
  if (!profile) {
    res.status(404).json({ message: "Profile not found" });
    return;
  }
  res.json(profile);
});

export const listProfiles = asyncHandler(async (_req, res) => {
  const profiles = await UserProfile.find();
  res.json(profiles);
});

export const createProfile = asyncHandler(async (req, res) => {
  const { _id, ...payload } = req.body;
  if (_id) {
    const profile = await UserProfile.findByIdAndUpdate(_id, payload, {
      new: true,
      upsert: true,
      setDefaultsOnInsert: true,
    });
    res.status(200).json(profile);
  } else {
    const profile = await UserProfile.create(payload);
    res.status(201).json(profile);
  }
});

export const updateProfile = asyncHandler(async (req, res) => {
  const profile = await UserProfile.findByIdAndUpdate(req.params.id, req.body, {
    new: true,
  });
  res.json(profile);
});

export const deleteProfile = asyncHandler(async (req, res) => {
  await UserProfile.findByIdAndDelete(req.params.id);
  res.status(204).send();
});
