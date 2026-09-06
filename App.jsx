import { BrowserRouter, Routes, Route } from "react-router-dom";

import ReportLeak from "./pages/ReportLeak";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/report"
          element={<ReportLeak />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;