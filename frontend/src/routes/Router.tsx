import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Login } from "pages/login.page";
import { Dashboard } from "pages/dashboard.page";

export function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/login" element={<Login />} />

        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}