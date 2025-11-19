import { Router } from "express";
import { listJobs, createJob, updateJob, deleteJob } from "../controllers/jobsController";

const router = Router();

router.get("/", listJobs);
router.post("/", createJob);
router.put("/:id", updateJob);
router.delete("/:id", deleteJob);

export default router;
