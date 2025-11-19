import { BrowserRouter, Routes, Route } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppProvider } from "./context/AppContext";
import { AppShell } from "./components/layout/AppShell";
import { ProfileBuilder } from "./pages/ProfileBuilder";
import { RoleExplorer } from "./pages/RoleExplorer";
import { RoadmapView } from "./pages/RoadmapView";
import { JobsBoard } from "./pages/JobsBoard";
import { Dashboard } from "./pages/Dashboard";

const queryClient = new QueryClient();

export const App = () => {
  return (
    <QueryClientProvider client={queryClient}>
      <AppProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<AppShell />}>
              <Route index element={<ProfileBuilder />} />
              <Route path="roles" element={<RoleExplorer />} />
              <Route path="roadmap" element={<RoadmapView />} />
              <Route path="jobs" element={<JobsBoard />} />
              <Route path="dashboard" element={<Dashboard />} />
            </Route>
          </Routes>
        </BrowserRouter>
      </AppProvider>
    </QueryClientProvider>
  );
};
