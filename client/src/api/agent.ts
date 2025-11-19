import { agentClient } from "./httpClient";
import { SeekerProfile } from "../context/AppContext";

export const fetchRoleFit = (profile: SeekerProfile) =>
  agentClient.post("/agents/role-fit", { seeker_profile: profile }).then((res) => res.data);

export const fetchRoadmap = (payload: { seeker_profile?: SeekerProfile; role_id?: string }) =>
  agentClient.post("/agents/roadmap", payload).then((res) => res.data);
