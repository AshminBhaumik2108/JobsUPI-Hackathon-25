import { NavLink, Outlet } from "react-router-dom";

const navItems = [
  { label: "Profile", path: "/" },
  { label: "Roles", path: "/roles" },
  { label: "Roadmap", path: "/roadmap" },
  { label: "Jobs", path: "/jobs" },
  { label: "Dashboard", path: "/dashboard" },
];

export const AppShell = () => {
  return (
    <div className="min-h-screen bg-slate-50">
      <header className="bg-white border-b border-slate-200 sticky top-0 z-50">
        <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
          <div className="text-2xl font-semibold text-slate-900">
            JobsUPI Seeker
          </div>
          <nav className="flex gap-4 text-sm font-medium text-slate-500">
            {navItems.map((item) => (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) =>
                  `rounded-full px-4 py-2 transition ${isActive ? "bg-brand-100 text-brand-600" : "hover:bg-slate-100"}`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-6xl px-6 py-10">
        <Outlet />
      </main>
    </div>
  );
};
