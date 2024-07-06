const express = require("express");
const bodyParser = require("body-parser");
const fs = require("fs");
const WebSocket = require("ws");
const { createCanvas } = require("canvas");
const path = require("path");
const simpleheat = require("simpleheat");

const app = express();
const server = require("http").createServer(app);
const wss = new WebSocket.Server({ server });

app.use(bodyParser.json());

// Creating a json file for a authenticated user to store the user logs

wss.on("connection", (ws) => {
  console.log("Client connected");

  ws.on("message", (message) => {
    const data = JSON.parse(message);
    const userId = data.userId;

    const filePath = path.join(__dirname, `${userId}-activityLog.json`);

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
  });
});

/**
 * this api returns the heatmap image for a authenticated user
 * @description getting user id in params for now but in future it should be extract from auth session
 */
app.get("/heatmap/:userId", (req, res) => {
  const userId = req.params.userId;
  const filePath = path.join(__dirname, `${userId}-activityLog.json`);

  if (!fs.existsSync(filePath)) {
    return res.status(404).send("No activity logs found for this user.");
  }

  const activityLogs = JSON.parse(fs.readFileSync(filePath));

  const canvas = createCanvas(1920, 1080);
  const ctx = canvas.getContext("2d");

  const heatmapData = activityLogs
    .filter((log) => log.type === "mousemove")
    .map((log) => [log.details.x, log.details.y, 1]);

  const heat = simpleheat(canvas);
  heat.data(heatmapData);
  heat.max(10);
  heat.draw();

  const out = fs.createWriteStream(path.join(__dirname, "heatmap.png"));
  const stream = canvas.createPNGStream();
  stream.pipe(out);

  out.on("finish", () => {
    res.sendFile(path.join(__dirname, "heatmap.png"));
  });
});
server.listen(3000, () => {
  console.log("Server is running on port 3000");
});
