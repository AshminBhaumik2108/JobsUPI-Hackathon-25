import { Router } from "express";
import profilesRoutes from "./profiles";
import rolesRoutes from "./roles";
import roadmapsRoutes from "./roadmaps";
import jobsRoutes from "./jobs";

const router = Router();

router.use("/profiles", profilesRoutes);
router.use("/roles", rolesRoutes);
router.use("/roadmaps", roadmapsRoutes);
router.use("/jobs", jobsRoutes);

export default router;
