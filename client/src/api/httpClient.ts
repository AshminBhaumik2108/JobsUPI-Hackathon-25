import axios from "axios";

const agentBaseUrl = import.meta.env.VITE_AGENT_API_URL || "http://localhost:8001";
const coreBaseUrl = import.meta.env.VITE_CORE_API_URL || "http://localhost:3002/api/v1";

export const agentClient = axios.create({ baseURL: agentBaseUrl });
export const coreClient = axios.create({ baseURL: coreBaseUrl });
