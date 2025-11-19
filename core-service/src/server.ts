import "dotenv/config";
import apiRouter from './routes';
import express from "express";
import cors from "cors";
import { connectDatabase } from "../config/database";

const app = express();

const allowedOrigins = process.env.ALLOWED_ORIGINS?.split(",") || ["http://localhost:5173"];
app.use(
  cors({
    origin: allowedOrigins,
    credentials: true,
  })
);
app.use(express.json());

app.use("/api/v1", apiRouter);

app.get("/health", (_req, res) => {
  res.status(200).send("Healthy");
});

const PORT = process.env.PORT || 3002;
const URL = process.env.APPLICATION || "http://localhost";

connectDatabase().then(() => {
  app.listen(PORT, () => {
    console.log(`SERVER listening on ${URL}:${PORT}`);
  });
});

export default app;
