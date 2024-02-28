// Importing modules
import React, { useState } from "react";
import "./App.css";

function App() {
  // useState for setting a JavaScript object for storing and using data
  const [data, setData] = useState({
    Date: "",
    summary: "",
    errors: {},
    alerts: {},
    features: {},
    rating: 0,
  });

  const [urlInput, setUrlInput] = useState(""); // State for storing the URL input
  const [error, setError] = useState(null); // State for handling errors
  const [showReport, setShowReport] = useState(false); // State to toggle report visibility

  // Function to handle fetching data based on the input URL
  const fetchData = async () => {
    try {
      if (urlInput.trim() !== "") {
        const res = await fetch(`/report?url=${urlInput}`);
        const jsonData = await res.json();
        console.log("Received data:", jsonData);
        setData(jsonData);
        setError(null); // Resetting error state on successful fetch
        setShowReport(true); // Show the report after successful fetch
      } else {
        setError("Please enter a valid URL");
        setShowReport(false); // Hide the report if there's an error
      }
    } catch (error) {
      console.error("Error fetching data:", error);
      setError("Error fetching data. Please try again.");
      setShowReport(false); // Hide the report if there's an error
    }
  };

  return (
    <div className="App">
      <div className="container" style={{ flex: 1 }}>
        <header className="App-header">
          <h1 className="display-4">Accessibility Checker</h1>
          {/* Input field for URL */}
          <div>
            <input
              type="text"
              className="form-control"
              placeholder="Enter URL"
              value={urlInput}
              onChange={(e) => setUrlInput(e.target.value)}
            />
            <div className="input-group-append">
              {/* Button to trigger fetching data */}
              <button
                className="btn btn-primary"
                type="button"
                onClick={fetchData}
              >
                Fetch Data
              </button>
            </div>
          </div>
          {/* Displaying fetched data or error message */}
          {!showReport ? (
            <p className="lead">{error ? error : "No data to display"}</p>
          ) : (
            <div>
              <p>Date: {data.Date}</p>

              <h2>Report</h2>
              {data && data.summary ? (
                <p>Summary: {data.summary}</p>
              ) : (
                <p>No summary available</p>
              )}

              <h2>Errors</h2>
              <ul>
                {data &&
                  data.errors &&
                  Object.entries(data.errors).map(([errorType, count]) => (
                    <li key={errorType}>{`${errorType}: ${count}`}</li>
                  ))}
              </ul>

              <h2>Alerts</h2>
              <ul>
                {data &&
                  data.alerts &&
                  Object.entries(data.alerts).map(([alertType, count]) => (
                    <li key={alertType}>{`${alertType}: ${count}`}</li>
                  ))}
              </ul>

              <h2>Features</h2>
              <ul>
                {data &&
                  data.features &&
                  Object.entries(data.features).map(([featureType, count]) => (
                    <li key={featureType}>{`${featureType}: ${count}`}</li>
                  ))}
              </ul>

              <h2>Rating</h2>
              {/* show rating if not undefined */}
              {data && data.rating !== undefined ? (
                <p>Rating: {data.rating}</p>
              ) : (
                <p>No rating available</p>
              )}
            </div>
          )}
        </header>
      </div>
    </div>
  );
}

export default App;
