import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
} from "react-leaflet";

import L from "leaflet";

import "leaflet/dist/leaflet.css";

// =========================================================
// CURRENT LOCATION MAP
// =========================================================

function MapView({ location }) {
  if (!location) {
    return null;
  }

  const locationIcon = L.divIcon({
    className: "current-location-marker",

    html: `
      <div
        style="
          width: 22px;
          height: 22px;
          background: #3b82f6;
          border: 4px solid white;
          border-radius: 50%;
          box-shadow: 0 2px 10px rgba(0,0,0,0.35);
        "
      ></div>
    `,

    iconSize: [22, 22],
    iconAnchor: [11, 11],
  });

  return (
    <div
      style={{
        width: "100%",
        height: "100%",
        border: "3px solid #38bdf8",
        borderRadius: "18px",
        overflow: "hidden",
        boxSizing: "border-box",
        boxShadow: "0 6px 18px rgba(56, 189, 248, 0.25)",
      }}
    >
      <MapContainer
        center={[location.latitude, location.longitude]}
        zoom={16}
        scrollWheelZoom={true}
        style={{
          width: "100%",
          height: "100%",
          minHeight: "330px",
        }}
      >

        {/* OPENSTREETMAP */}

        <TileLayer
          attribution="&copy; OpenStreetMap contributors"
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {/* CURRENT LOCATION */}

        <Marker
          position={[
            location.latitude,
            location.longitude,
          ]}
          icon={locationIcon}
        >
          <Popup>
            <strong>Your Current Location</strong>
            <br />
            Latitude: {location.latitude.toFixed(6)}
            <br />
            Longitude: {location.longitude.toFixed(6)}
          </Popup>
        </Marker>

      </MapContainer>
    </div>
  );
}

export default MapView;