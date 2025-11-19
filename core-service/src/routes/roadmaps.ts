import { Router } from "express";
import { listRoadmaps, getRoadmapById, createRoadmap } from "../controllers/roadmapsController";

const router = Router();

router.get("/", listRoadmaps);
router.get("/:id", getRoadmapById);
router.post("/", createRoadmap);

export default router;
