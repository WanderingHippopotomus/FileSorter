import { useState, useRef, useEffect, useCallback } from "react";
import {
  Folder,
  FolderOpen,
  Image,
  Film,
  Music,
  FileText,
  Archive,
  Terminal,
  Code2,
  Package,
  CheckCircle,
  Circle,
  AlertTriangle,
  Loader2,
  Minus,
  Square,
  X,
  Sparkles,
} from "lucide-react";

import "./App.css";

const electronAPI = window?.electronAPI;

function TitleBar() {
  const handleMinimize = () => electronAPI?.minimize?.();
  const handleMaximize = () => electronAPI?.maximize?.();
  const handleClose = () => electronAPI?.close?.();

  return (
    <div className="title-bar">
      <div className="title-bar-left">
        <Folder size={14} />
        <span>File Sorter</span>
      </div>

      <div className="title-bar-controls">
        <button className="win-btn" onClick={handleMinimize} aria-label="Minimize">
          <Minus size={14} />
        </button>
        <button className="win-btn" onClick={handleMaximize} aria-label="Maximize">
          <Square size={10} />
        </button>
        <button className="win-btn close" onClick={handleClose} aria-label="Close">
          <X size={14} />
        </button>
      </div>
    </div>
  );
}

function useCountUp(value, duration = 450) {
  const [display, setDisplay] = useState(value);
  const frame = useRef(null);

  useEffect(() => {
    const start = display;
    const change = value - start;

    if (change === 0) return;

    const startTime = performance.now();

    const tick = (now) => {
      const progress = Math.min((now - startTime) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3);

      setDisplay(Math.round(start + change * eased));

      if (progress < 1) {
        frame.current = requestAnimationFrame(tick);
      }
    };

    frame.current = requestAnimationFrame(tick);

    return () => cancelAnimationFrame(frame.current);
  }, [value, duration]);

  return display;
}

function App() {
  const [folder, setFolder] = useState("C:\\Users\\HP\\Downloads");
  const [status, setStatus] = useState("Ready");
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [isDragActive, setIsDragActive] = useState(false);

  const [stats, setStats] = useState({
    images: 0,
    videos: 0,
    audios: 0,
    documents: 0,
    archives: 0,
    executables: 0,
    codes: 0,
    others: 0,
  });

  const images = useCountUp(stats.images);
  const videos = useCountUp(stats.videos);
  const audios = useCountUp(stats.audios);
  const documents = useCountUp(stats.documents);
  const archives = useCountUp(stats.archives);
  const executables = useCountUp(stats.executables);
  const codes = useCountUp(stats.codes);
  const others = useCountUp(stats.others);

  const progressTimer = useRef(null);

  const [apiBase, setApiBase] = useState(null);
  const [backendReady, setBackendReady] = useState(false);
  const [backendFailed, setBackendFailed] = useState(false);

  // Step 1 + 2: resolve the port, then poll that address until the backend responds.
  useEffect(() => {
    let cancelled = false;

    async function resolvePortAndPoll() {
      // In production, main.js spawned the backend and knows its real port.
      // In dev, nothing was spawned — fall back to the port you run uvicorn on manually.
      let port = null;
      try {
        console.log("electronAPI:", electronAPI);
        console.log("getBackendPort:", electronAPI?.getBackendPort);
        port = await electronAPI?.getBackendPort?.();
      } catch {
        // ignore — treated as "no port available" below
      }

      const resolvedPort = port ?? 8000;
      const base = `http://127.0.0.1:${resolvedPort}`;

      if (cancelled) return;
      setApiBase(base);

      let attempts = 0;
      const maxAttempts = 40; // ~20s at 500ms intervals

      while (!cancelled && attempts < maxAttempts) {
        attempts++;
        try {
          const res = await fetch(`${base}/api/default-dir`);
          if (res.ok) {
            if (!cancelled) setBackendReady(true);
            return;
          }
        } catch {
          // not up yet, keep trying
        }
        await new Promise((r) => setTimeout(r, 500));
      }

      if (!cancelled) setBackendFailed(true);
    }

    resolvePortAndPoll();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    return () => clearInterval(progressTimer.current);
  }, []);

  const isError = status === "Backend Offline";

  async function chooseFolder() {
    if (!apiBase) return;
    try {
      const response = await fetch(`${apiBase}/api/browse`);

      if (!response.ok) {
        throw new Error("Unable to browse folders.");
      }

      const data = await response.json();

      if (data.path) {
        setFolder(data.path);
      }
    } catch {
      alert("Unable to open folder picker. Is the backend running?");
    }
  }

  function simulateProgress() {
    setProgress(0);

    progressTimer.current = setInterval(() => {
      setProgress((p) => (p >= 90 ? p : p + Math.random() * 12));
    }, 220);
  }

  function stopProgress(finalValue) {
    clearInterval(progressTimer.current);
    setProgress(finalValue);
  }

  async function sortFiles(targetFolder = folder) {
    if (!apiBase) return;

    setLoading(true);
    setStatus("Sorting...");
    simulateProgress();

    try {
      const response = await fetch(`${apiBase}/api/sort`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          directory: targetFolder,
        }),
      });

      if (!response.ok) {
        throw new Error("Sorting failed.");
      }

      const data = await response.json();

      console.log("Backend response:", data);

      setStats(data.breakdown);

      stopProgress(100);
      setStatus("Completed");
    } catch {
      stopProgress(0);
      setStatus("Backend Offline");
    }

    setLoading(false);
  }

  const handleDragOver = useCallback((e) => {
    e.preventDefault();
    setIsDragActive(true);
  }, []);

  const handleDragLeave = useCallback(() => {
    setIsDragActive(false);
  }, []);

  const handleDrop = useCallback(
    (e) => {
      e.preventDefault();
      setIsDragActive(false);

      const item = e.dataTransfer.files?.[0];

      if (!item) return;

      const path = electronAPI?.getPathForFile?.(item);

      if (path) {
        setFolder(path);
        sortFiles(path);
      } else {
        alert("Couldn't resolve the dropped folder's path.");
      }
    },
    [folder]
  );

  return (
    <div className="app-shell">
      <TitleBar />

      <div className="content">
        <div className="window">
          <header className="header">
            <div className="title">
              <div className="title-icon-wrap">
                <Folder size={18} />
              </div>

              <h1>File Sorter</h1>
            </div>

            <span className="author">by Kushagra Shrivastava</span>
          </header>
          {!backendReady ? (
            <section className="panel loading-panel">
              {backendFailed ? (
                <>
                  <AlertTriangle size={22} />
                  <p>Backend failed to start.</p>
                  <span className="loading-sub">Try restarting the app.</span>
                </>
              ) : (
                <>
                  <Loader2 className="spin" size={22} />
                  <p>Starting up…</p>
                  <span className="loading-sub">Waking up the backend</span>
                </>
              )}
            </section>
          ) : (
            <section className="panel">
              <div>
                <div className="section-title">Folder</div>

                <div className="folder-container">
                  <input
                    value={folder}
                    onChange={(e) => setFolder(e.target.value)}
                    placeholder="Choose a folder to sort"
                  />

                  <button className="browse-btn" onClick={chooseFolder}>
                    <FolderOpen size={16} />
                  </button>
                </div>
              </div>

              <div
                className={`drop-zone ${isDragActive ? "active" : ""}`}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
              >
                Drag a folder here to sort it instantly
              </div>

              <div>
                <div className="section-title">Status</div>

                <div className={`status ${isError ? "error" : ""}`}>
                  {loading ? (
                    <Loader2 className="spin" size={16} />
                  ) : isError ? (
                    <AlertTriangle size={16} />
                  ) : status === "Completed" ? (
                    <CheckCircle size={16} />
                  ) : (
                    <Circle size={12} />
                  )}

                  <span>{status}</span>
                </div>

                {loading && (
                  <div className="progress-track">
                    <div
                      className="progress-fill"
                      style={{ width: `${progress}%` }}
                    />
                  </div>
                )}
              </div>

              <div>
                <div className="section-title">Statistics</div>

                <div className="stats-grid">
                  <div className="stat-card">
                    <Image size={15} />
                    <strong>{images}</strong>
                    <span>Images</span>
                  </div>

                  <div className="stat-card">
                    <Film size={15} />
                    <strong>{videos}</strong>
                    <span>Videos</span>
                  </div>

                  <div className="stat-card">
                    <Music size={15} />
                    <strong>{audios}</strong>
                    <span>Audio</span>
                  </div>

                  <div className="stat-card">
                    <FileText size={15} />
                    <strong>{documents}</strong>
                    <span>Docs</span>
                  </div>

                  <div className="stat-card">
                    <Archive size={15} />
                    <strong>{archives}</strong>
                    <span>Archives</span>
                  </div>

                  <div className="stat-card">
                    <Terminal size={15} />
                    <strong>{executables}</strong>
                    <span>Exe</span>
                  </div>

                  <div className="stat-card">
                    <Code2 size={15} />
                    <strong>{codes}</strong>
                    <span>Code</span>
                  </div>

                  <div className="stat-card">
                    <Package size={15} />
                    <strong>{others}</strong>
                    <span>Others</span>
                  </div>
                </div>
              </div>

              <button
                className="sort-btn"
                disabled={loading}
                onClick={() => sortFiles()}
              >
                {loading ? (
                  <>
                    <Loader2 className="spin" size={16} />
                    Sorting...
                  </>
                ) : (
                  <>
                    <Sparkles size={16} />
                    Sort Files
                  </>
                )}
              </button>
            </section>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;