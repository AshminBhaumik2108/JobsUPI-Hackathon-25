import "dotenv/config";
import { connectDatabase, disconnectDatabase } from "../config/database";
import { RoleTemplate } from "../src/schemas/RoleTemplate";
import { JobPosting } from "../src/schemas/JobPosting";

const roles = [{
  title: "MERN Support Intern",
  description: "Support the MERN stack portal with frontend and backend fixes.",
  skills: { mustHave: ["javascript", "html"], niceToHave: ["mongodb"] },
  personality: ["detail-oriented", "curious"],
  environment: { mobility: "low" },
  roadmap: [
    { title: "Frontend refresh", description: "Revisit React + Tailwind basics to support UI fixes in the MERN stack portal.", durationWeeks: 2, resources: ["JobsUPI React snippets", "Vite/Tailwind crash course"] },
    { title: "API ticket drills", description: "Shadow senior devs to triage Express/Mongo API bugs and log AI-agent issues.", durationWeeks: 2, resources: ["Postman collections", "GitHub issue templates"] },
  ],
}];

const seed = async () => {
  await connectDatabase();
  await RoleTemplate.deleteMany({});
  await JobPosting.deleteMany({});
  const createdRoles = await RoleTemplate.insertMany(roles);
  await JobPosting.insertMany(
    createdRoles.map((role) => ({
      role: role._id,
      employer: "Sample Employer",
      location: "Kolkata",
      salaryMin: 15000,
      salaryMax: 20000,
    }))
  );
  await disconnectDatabase();
  console.log("Seed completed");
};

seed().catch((err) => {
  console.error(err);
  process.exit(1);
});
