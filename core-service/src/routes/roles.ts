import { Router } from "express";
import { listRoles, getRole, createRole } from "../controllers/rolesController";

const router = Router();

router.get("/", listRoles);
router.get("/:id", getRole);
router.post("/", createRole);

export default router;
