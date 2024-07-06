const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const WebSocket = require("ws");
const path = require("path");
const { generateHeatmap } = require("./heatmap");

const app = express();
const server = require("http").createServer(app);
const wss = new WebSocket.Server({ server });

app.use(express.static("public"));

app.use(bodyParser.json());

// Creating a json file for a authenticated user to store the user logs

wss.on("connection", (ws) => {
  try {
    console.log("Client connected");
    let userId = null;
    ws.on("message", (message) => {
      const data = JSON.parse(message);
      userId = data.userId;

      const filePath = path.join(
        __dirname,
        "activity_logs",
        `${userId}-activityLog.json`
      );

      let userLogs = [];

      if (fs.existsSync(filePath)) {
        const existingLogs = fs.readFileSync(filePath);
        userLogs = JSON.parse(existingLogs);
      }

      userLogs.push(...data.activityLogs);

      fs.writeFileSync(filePath, JSON.stringify(userLogs));
    });

    ws.on("close", () => {
      console.log("Client disconnected");
      generateHeatmap(userId);
      console.log("Heatmap generated");
      fs.unlink(
        path.join(__dirname, "activity_logs", userId + "-activityLog.json"),
        (err) => {
          console.log("err=", err);
        }
      );
    });
  } catch (error) {
    console.log({ error });
  }
});

server.listen(3000, () => {
  console.log("Server is running on port 3000");
});
