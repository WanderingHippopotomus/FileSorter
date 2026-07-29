const { app, BrowserWindow, ipcMain, dialog } = require("electron");
const { spawn } = require("child_process");
const path = require("path");
const fs = require("fs");

const isDev = !app.isPackaged;

let backend;
let backendPort = null;

function startBackend() {
  console.log("========== startBackend ==========");
  console.log("isDev:", isDev);

  if (isDev) {
    console.log("Development mode, not spawning backend.");
    return;
  }

  const backendPath = path.join(process.resourcesPath, "backend", "backend.exe");

  console.log("resourcesPath:", process.resourcesPath);
  console.log("backendPath:", backendPath);
  console.log("exists:", fs.existsSync(backendPath));

  backend = spawn(backendPath, [], {
    cwd: path.dirname(backendPath),
    stdio: "pipe",
  });

  console.log("spawn() returned");

  backend.stdout.on("data", (data) => {
    const text = data.toString();
    console.log("[Backend]", text);

    const match = text.match(/PORT:(\d+)/);
    if (match) {
      backendPort = parseInt(match[1], 10);
      console.log("Backend port detected:", backendPort);
    }
  });

  backend.stderr.on("data", (data) =>
    console.error("[Backend Error]", data.toString())
  );

  backend.on("error", (err) => {
    console.error("Spawn error:", err);
    dialog.showErrorBox("Startup Error", `Couldn't start backend:\n${err.message}`);
  });

  backend.on("exit", (code, signal) => {
    console.log("Backend exited");
    console.log("Code:", code);
    console.log("Signal:", signal);
  });
}

function createWindow() {
  const win = new BrowserWindow({
    width: 520,
    height: 860,
    resizable: false,
    maximizable: false,
    fullscreenable: false,
    autoHideMenuBar: true,
    frame: false,
    title: "File Sorter",
    backgroundColor: "#f5f5f7",
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, "preload.js"),
    },
  });

  if (isDev) {
    win.loadURL("http://localhost:5173");
  } else {
    win.loadFile(path.join(__dirname, "../frontend/dist/index.html"));
  }

  return win;
}

const gotLock = app.requestSingleInstanceLock();

if (!gotLock) {
  app.quit();
} else {
  app.on("second-instance", () => {
    const win = BrowserWindow.getAllWindows()[0];
    if (win) {
      if (win.isMinimized()) win.restore();
      win.focus();
    }
  });

  ipcMain.on("window-minimize", () => {
    BrowserWindow.getFocusedWindow()?.minimize();
  });

  ipcMain.on("window-maximize", () => {
    const win = BrowserWindow.getFocusedWindow();
    if (!win) return;
    if (win.isMaximizable()) {
      win.isMaximized() ? win.unmaximize() : win.maximize();
    }
  });

  ipcMain.on("window-close", () => {
    BrowserWindow.getFocusedWindow()?.close();
  });

  ipcMain.handle("get-backend-port", async () => {
  while (backendPort === null) {
    await new Promise(r => setTimeout(r, 100));
  }
  return backendPort;
});

  app.whenReady().then(() => {
    startBackend();
    createWindow();
  });

  app.on("will-quit", () => {
    if (backend && !backend.killed) {
      backend.kill();
    }
  });

  app.on("window-all-closed", () => {
    if (process.platform !== "darwin") {
      app.quit();
    }
  });
}