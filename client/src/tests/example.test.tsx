import { describe, expect, it } from "vitest";
import { render, screen } from "@testing-library/react";
import { App } from "../App";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { AppProvider } from "../context/AppContext";

const queryClient = new QueryClient();

describe("App", () => {
  it("renders header", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <AppProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </AppProvider>
      </QueryClientProvider>
    );
    expect(screen.getByText(/JobsUPI Seeker/i)).toBeInTheDocument();
  });
});
