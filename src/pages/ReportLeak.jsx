import { useEffect, useState } from "react";
import MapView from "../components/MapView";
import IncidentMap from "../components/IncidentMap";
import "./ReportLeak.css";

function ReportLeak() {
  const [location, setLocation] = useState(null);
  const [locationLoading, setLocationLoading] = useState(true);
  const [locationError, setLocationError] = useState("");

  const [images, setImages] = useState([]);
  const [problemType, setProblemType] = useState("Waterlogging");
  const [severity, setSeverity] = useState("Medium");
  const [description, setDescription] = useState("");
  const [submitted, setSubmitted] = useState(false);

  // ==========================================
  // GET CURRENT LOCATION
  // ==========================================
  const getLocation = () => {
    setLocationLoading(true);
    setLocationError("");

    if (!navigator.geolocation) {
      setLocationError(
        "Geolocation is not supported by this browser."
      );
      setLocationLoading(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          latitude: position.coords.latitude,
          longitude: position.coords.longitude,
          accuracy: position.coords.accuracy,
        });

        setLocationLoading(false);
      },
      (error) => {
        console.log(error);

        setLocationError(
          "Unable to detect your location. Please allow location access."
        );

        setLocationLoading(false);
      }
    );
  };

  useEffect(() => {
    getLocation();
  }, []);

  // ==========================================
  // IMAGE UPLOAD
  // ==========================================
  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);

    if (files.length === 0) return;

    const invalid = files.find(
      (file) => !file.type.startsWith("image/")
    );

    if (invalid) {
      alert("Please upload only image files.");
      return;
    }

    if (images.length + files.length > 5) {
      alert("Maximum 5 photos allowed.");
      return;
    }

    setImages((prev) => [...prev, ...files]);

    e.target.value = "";
  };

  // ==========================================
  // REMOVE IMAGE
  // ==========================================
  const removeImage = (index) => {
    setImages((prev) =>
      prev.filter((_, imageIndex) => imageIndex !== index)
    );
  };

  // ==========================================
  // SUBMIT REPORT
  // ==========================================
  const handleSubmit = (event) => {
    event.preventDefault();

    if (!location) {
      alert("Please wait until your location is detected.");
      return;
    }

    if (!description.trim()) {
      alert("Please describe the water problem.");
      return;
    }

    const reportData = {
      problemType,
      severity,
      description,
      images,
      location,
    };

    console.log("Report submitted:", reportData);

    setSubmitted(true);
  };

  return (
    <div className="civic-page">

      {/* ==========================================
          HEADER
      ========================================== */}
      <header className="civic-header">

        <div className="brand-area">

          <div className="brand-logo">
            CP
          </div>

          <div>
            <div className="brand-name">
              CivicPulse
            </div>

            <div className="brand-subtitle">
              AI-Powered Civic Intelligence
            </div>
          </div>

        </div>

        <div className="header-tag">
          <span>●</span>
          Live Civic Monitoring
        </div>

      </header>


      {/* ==========================================
          HERO
      ========================================== */}
      <section className="hero-section">

        <div className="hero-badge">
          🚨 Civic Issue Reporting
        </div>

        <h1>
          Report a Water Problem
        </h1>

        <p>
          Help improve your community by reporting water,
          drainage, and infrastructure problems.
        </p>

        <div className="hero-features">

          <div className="hero-feature">

            <span>📍</span>

            <div>
              <strong>Precise Location</strong>
              <small>GPS automatically captured</small>
            </div>

          </div>

          <div className="feature-divider"></div>

          <div className="hero-feature">

            <span>📷</span>

            <div>
              <strong>Visual Evidence</strong>
              <small>Upload up to 5 photos</small>
            </div>

          </div>

          <div className="feature-divider"></div>

          <div className="hero-feature">

            <span>🤖</span>

            <div>
              <strong>AI Analysis</strong>
              <small>Reports intelligently correlated</small>
            </div>

          </div>

        </div>

      </section>


      {/* ==========================================
          MAIN CONTENT
      ========================================== */}
      <main className="report-container">

        <form onSubmit={handleSubmit}>


          {/* ==========================================
              LOCATION CARD
          ========================================== */}
          <section className="glass-card location-card">

            <div className="section-heading">

              <div className="section-icon location-icon">
                📍
              </div>

              <div>
                <h2>Location</h2>

                <p>
                  Your current location helps authorities
                  identify the exact issue.
                </p>
              </div>

            </div>


            {/* LOCATION LOADING */}
            {locationLoading && (

              <div className="location-status loading">

                <div className="status-icon">
                  📡
                </div>

                <div>

                  <strong>
                    Detecting your location...
                  </strong>

                  <p>
                    Please allow location access in your browser.
                  </p>

                </div>

              </div>

            )}


            {/* LOCATION ERROR */}
            {locationError && (

              <div className="location-status error-location">

                <div className="status-icon">
                  ⚠️
                </div>

                <div>

                  <strong>
                    Location could not be detected
                  </strong>

                  <p>
                    {locationError}
                  </p>

                  <button
                    type="button"
                    onClick={getLocation}
                    className="retry-button"
                  >
                    Try Again
                  </button>

                </div>

              </div>

            )}


            {/* ==========================================
                LOCATION SUCCESS
            ========================================== */}
            {location && (

              <div className="location-layout">

                {/* ======================================
                    LEFT SIDE
                ====================================== */}
                <div className="location-left">

                  {/* SUCCESS MESSAGE */}
                  <div className="location-status success-location">

                    <div className="status-icon">
                      ✓
                    </div>

                    <div>

                      <strong>
                        Location detected successfully
                      </strong>

                      <p>
                        Your location has been captured for this report.
                      </p>

                    </div>

                  </div>


                  {/* LOCATION DETAILS */}
                  <div className="location-stats">


                    {/* LATITUDE */}
                    <div className="location-stat">

                      <span className="stat-icon blue">
                        N
                      </span>

                      <div>

                        <small>
                          Latitude
                        </small>

                        <strong>
                          {location.latitude.toFixed(6)}
                        </strong>

                      </div>

                    </div>


                    {/* LONGITUDE */}
                    <div className="location-stat">

                      <span className="stat-icon green">
                        E
                      </span>

                      <div>

                        <small>
                          Longitude
                        </small>

                        <strong>
                          {location.longitude.toFixed(6)}
                        </strong>

                      </div>

                    </div>


                    {/* ACCURACY */}
                    <div className="location-stat">

                      <span className="stat-icon purple">
                        ±
                      </span>

                      <div>

                        <small>
                          Accuracy
                        </small>

                        <strong>
                          ~{Math.round(location.accuracy)} meters
                        </strong>

                      </div>

                    </div>

                  </div>

                </div>


                {/* ======================================
                    RIGHT SIDE - MAP
                ====================================== */}
                <div className="map-wrapper">

                  <MapView location={location} />

                </div>

              </div>

            )}

          </section>


          {/* ==========================================
              CIVICPULSE INCIDENT INTELLIGENCE MAP
          ========================================== */}
          <section className="glass-card incident-intelligence-card">

            <div className="section-heading">

              <div className="section-icon">
                🧠
              </div>

              <div>

                <h2>
                  CivicPulse Incident Intelligence
                </h2>

                <p>
                  View correlated civic incidents detected
                  across the monitored area.
                </p>

              </div>

            </div>


            {/* INCIDENT LEGEND */}
            <div className="incident-map-info">

              <div className="incident-info-item">

                <span className="info-dot critical"></span>

                <div>
                  <strong>Critical</strong>
                  <small>Severity 90+</small>
                </div>

              </div>


              <div className="incident-info-item">

                <span className="info-dot high"></span>

                <div>
                  <strong>High</strong>
                  <small>Severity 60–89</small>
                </div>

              </div>


              <div className="incident-info-item">

                <span className="info-dot monitoring"></span>

                <div>
                  <strong>Monitoring</strong>
                  <small>Severity below 50</small>
                </div>

              </div>

            </div>


            {/* INCIDENT MAP */}
            <div className="incident-map-wrapper">

              <IncidentMap />

            </div>

          </section>


          {/* ==========================================
              PHOTO + DETAILS
          ========================================== */}
          <div className="form-grid">


            {/* ======================================
                PHOTO CARD
            ====================================== */}
            <section className="glass-card photo-card">

              <div className="section-heading">

                <div className="section-icon photo-icon">
                  📷
                </div>

                <div>

                  <h2>
                    Photos
                  </h2>

                  <p>
                    Add photos showing the water problem.
                  </p>

                </div>

              </div>


              <div className="upload-box">

                <div className="upload-icon">
                  🖼️
                </div>

                <h3>
                  Upload photos
                </h3>

                <p>
                  JPG, PNG or other image formats
                </p>

                <label className="choose-photo">

                  🖼️ Choose Photos

                  <input
                    type="file"
                    multiple
                    accept="image/*"
                    onChange={handleImageChange}
                  />

                </label>

                <small>
                  {images.length}/5 photos selected
                </small>

              </div>


              {/* PHOTO PREVIEWS */}
              {images.length > 0 && (

                <div className="photo-preview-grid">

                  {images.map((image, index) => (

                    <div
                      className="photo-preview-card"
                      key={index}
                    >

                      <img
                        src={URL.createObjectURL(image)}
                        alt={`Preview ${index + 1}`}
                      />

                      <button
                        type="button"
                        className="remove-photo-btn"
                        onClick={() => removeImage(index)}
                      >
                        ✕
                      </button>

                      <div className="photo-number">
                        Photo {index + 1}
                      </div>

                    </div>

                  ))}

                </div>

              )}

            </section>


            {/* ======================================
                DETAILS CARD
            ====================================== */}
            <section className="glass-card details-card">

              <div className="section-heading">

                <div className="section-icon details-icon">
                  📋
                </div>

                <div>

                  <h2>
                    Problem Details
                  </h2>

                  <p>
                    Tell us what is happening.
                  </p>

                </div>

              </div>


              <div className="details-form">


                {/* PROBLEM TYPE */}
                <div className="field-group">

                  <label>
                    Problem Type
                  </label>

                  <select
                    value={problemType}
                    onChange={(event) =>
                      setProblemType(event.target.value)
                    }
                  >

                    <option value="Waterlogging">
                      Waterlogging
                    </option>

                    <option value="Water Leakage">
                      Water Leakage
                    </option>

                    <option value="Pipe Burst">
                      Pipe Burst
                    </option>

                    <option value="Drainage Problem">
                      Drainage Problem
                    </option>

                    <option value="Sewage Overflow">
                      Sewage Overflow
                    </option>

                    <option value="Damaged Water Pipe">
                      Damaged Water Pipe
                    </option>

                    <option value="Other">
                      Other
                    </option>

                  </select>

                </div>


                {/* SEVERITY */}
                <div className="field-group">

                  <label>
                    Severity
                  </label>

                  <select
                    value={severity}
                    onChange={(event) =>
                      setSeverity(event.target.value)
                    }
                  >

                    <option value="Low">
                      Low
                    </option>

                    <option value="Medium">
                      Medium
                    </option>

                    <option value="High">
                      High
                    </option>

                    <option value="Critical">
                      Critical
                    </option>

                  </select>

                  <div className="severity-help">
                    Select how serious the problem is.
                  </div>

                </div>


                {/* DESCRIPTION */}
                <div className="field-group description-field">

                  <label>
                    Describe the Problem
                  </label>

                  <textarea
                    value={description}
                    onChange={(event) =>
                      setDescription(event.target.value)
                    }
                    placeholder="Describe what is happening at this location..."
                    rows="7"
                    maxLength="500"
                  />

                  <div className="character-count">
                    {description.length}/500
                  </div>

                </div>

              </div>

            </section>

          </div>


          {/* ==========================================
              SUBMIT
          ========================================== */}
          <section className="glass-card submit-card">

            {!submitted ? (

              <div className="submit-content">

                <div>

                  <h2>
                    Ready to submit?
                  </h2>

                  <p>
                    Your report will be processed by
                    CivicPulse's intelligence system.
                  </p>

                </div>

                <button
                  type="submit"
                  className="submit-button"
                >
                  🚨 Submit Report
                </button>

              </div>

            ) : (

              <div className="success-message">

                <div className="success-large-icon">
                  ✓
                </div>

                <div>

                  <h2>
                    Report Submitted Successfully!
                  </h2>

                  <p>
                    Your water problem has been recorded.
                    CivicPulse will process the report and
                    identify the appropriate response.
                  </p>

                </div>

              </div>

            )}

          </section>

        </form>

      </main>


      {/* ==========================================
          FOOTER
      ========================================== */}
      <footer className="civic-footer">

        <div className="footer-left">

          <strong>
            CivicPulse
          </strong>

          <span>
            AI-powered civic infrastructure intelligence
          </span>

        </div>

        <div className="footer-right">
          Improving cities, one report at a time.
        </div>

      </footer>

    </div>
  );
}

export default ReportLeak;