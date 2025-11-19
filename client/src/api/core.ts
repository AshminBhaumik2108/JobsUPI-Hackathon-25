import { coreClient } from "./httpClient";
import { SeekerProfile } from "../context/AppContext";

export const getProfileById = (id: string): Promise<SeekerProfile> =>
  coreClient.get(`/profiles/${id}`).then((res) => res.data);

export const createProfile = (profile: SeekerProfile) =>
  coreClient.post("/profiles", profile).then((res) => res.data);

export const updateProfile = (id: string, profile: Partial<SeekerProfile>) =>
  coreClient.put(`/profiles/${id}`, profile).then((res) => res.data);

export const getRoles = (params?: Record<string, string>) =>
  coreClient.get("/roles", { params }).then((res) => res.data);

export const getRoadmaps = (params?: Record<string, string>) =>
  coreClient.get("/roadmaps", { params }).then((res) => res.data);
export const createRoadmap = (payload: { role: string; userProfile: string; steps: any[] }) =>
  coreClient.post("/roadmaps", payload).then((res) => res.data);


export const getJobs = (params?: Record<string, string | number>) =>
  coreClient.get("/jobs", { params }).then((res) => res.data);
