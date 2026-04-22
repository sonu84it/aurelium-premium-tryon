import { createBrowserRouter } from "react-router-dom";

import { ResultsPage } from "@/pages/results-page";
import { LandingPage } from "@/pages/landing-page";
import { StudioPage } from "@/pages/studio-page";
import { UnsupportedPage } from "@/pages/unsupported-page";

export const router = createBrowserRouter([
  { path: "/", element: <LandingPage /> },
  { path: "/studio", element: <StudioPage /> },
  { path: "/results", element: <ResultsPage /> },
  { path: "/unsupported", element: <UnsupportedPage /> },
]);
