const { createCanvas } = require("canvas");
const simpleheat = require("simpleheat");
const path = require("path");
const fs = require("fs");

function generateHeatmap(userId) {
  const filePath = path.join(
    __dirname,
    "activity_logs",
    `${userId}-activityLog.json`
  );
  if (!fs.existsSync(filePath)) {
    return "No activity logs found for this user.";
  }

  const activityLogs = JSON.parse(fs.readFileSync(filePath));

  const canvas = createCanvas(1920, 1080);
  const ctx = canvas.getContext("2d");

  const heatmapData = activityLogs.map((log) => [
    log.details.x,
    log.details.y,
    1,
  ]);

  const heat = simpleheat(canvas);
  heat.data(heatmapData);
  heat.max(10);
  heat.draw();

  const _path = path.join(
    __dirname,
    "public",
    "users_heatmap",
    userId + "-heatmap.png"
  );
  const out = fs.createWriteStream(_path);
  console.log({ _path });
  const stream = canvas.createPNGStream();
  stream.pipe(out);

  out.on("finish", () => {
    return true;
  });
}
module.exports = { generateHeatmap };
