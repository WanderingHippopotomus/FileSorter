const { contextBridge, ipcRenderer, webUtils } = require("electron");

contextBridge.exposeInMainWorld("electronAPI", {
  minimize: () => ipcRenderer.send("window-minimize"),
  maximize: () => ipcRenderer.send("window-maximize"),
  close: () => ipcRenderer.send("window-close"),

  // Modern Electron strips File.path for security — this is the
  // sanctioned replacement, only usable from preload context.
  getPathForFile: (file) => webUtils.getPathForFile(file),

  // Reads the port the spawned backend reported via stdout (main.js parses "PORT:<n>").
  getBackendPort: () => ipcRenderer.invoke("get-backend-port"),
});