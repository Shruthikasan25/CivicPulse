import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";

import incidents from "../data/incidents.json";

// =========================================================
// CREATE COLORED MARKER
// =========================================================

const createMarker = (severity) => {
  let color = "#facc15"; // Yellow

  if (severity >= 90) {
    color = "#ef4444"; // Red
  } else if (severity >= 60) {
    color = "#f97316"; // Orange
  }

  return L.divIcon({
    className: "custom-incident-marker",

    html: `
      <div
        style="
          width: 22px;
          height: 22px;
          background: ${color};
          border: 3px solid white;
          border-radius: 50%;
          box-shadow: 0 2px 8px rgba(0,0,0,0.35);
        "
      ></div>
    `,

    iconSize: [22, 22],
    iconAnchor: [11, 11],
    popupAnchor: [0, -12],
  });
};

// =========================================================
// INCIDENT MAP
// =========================================================

function IncidentMap() {
  return (
    <div
      className="incident-map-container"
      style={{
        padding: "18px",
        boxSizing: "border-box",
      }}
    >

      <MapContainer
        center={[12.9737, 79.1636]}
        zoom={13}
        style={{
          width: "100%",
          height: "600px",

          /* WATER BLUE BORDER */
          border: "3px solid #38bdf8",

          borderRadius: "18px",
          overflow: "hidden",
          boxSizing: "border-box",

          /* SOFT WATER-BLUE GLOW */
          boxShadow: "0 6px 18px rgba(56, 189, 248, 0.25)",
        }}
      >

        {/* OPENSTREETMAP */}

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* INCIDENT PINS */}

        {incidents.map((incident) => (

          <Marker
            key={incident.incident_id}
            position={[
              incident.center_latitude,
              incident.center_longitude,
            ]}
            icon={createMarker(incident.severity_score)}
          >

            {/* POPUP */}

            <Popup>

              <div
                style={{
                  minWidth: "220px",
                  fontFamily: "Arial, sans-serif",
                }}
              >

                <h3
                  style={{
                    margin: "0 0 10px",
                    color: "#0f4c5c",
                  }}
                >
                  🚨 {incident.incident_id}
                </h3>

                <p>
                  <strong>Problem:</strong>{" "}
                  {incident.dominant_category.replaceAll(
                    "_",
                    " "
                  )}
                </p>

                <p>
                  <strong>Severity Score:</strong>{" "}
                  {incident.severity_score}
                </p>

                <p>
                  <strong>Reports Correlated:</strong>{" "}
                  {incident.total_reports_correlated}
                </p>

                <p
                  style={{
                    marginTop: "10px",
                    fontWeight: "bold",
                    color: "#0f4c5c",
                  }}
                >
                  {incident.total_reports_correlated} citizen
                  reports merged into this event.
                </p>

              </div>

            </Popup>

          </Marker>

        ))}

      </MapContainer>

      {/* =====================================================
          LEGEND
          ===================================================== */}

      <div className="incident-map-legend">

        <h3>Incident Severity</h3>

        <div className="legend-item">
          <span className="legend-dot critical"></span>
          <span>90+ — Critical</span>
        </div>

        <div className="legend-item">
          <span className="legend-dot high"></span>
          <span>60–89 — High</span>
        </div>

        <div className="legend-item">
          <span className="legend-dot monitoring"></span>
          <span>&lt;50 — Monitoring</span>
        </div>

      </div>

    </div>
  );
}

export default IncidentMap;