const express = require("express");
const Fuse = require("fuse.js");
const fs = require("fs");
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3002;

// Base URL untuk membuat link file
const BASE_URL = "http://pioneer.whatbox.ca:15735/mov/";

// Baca data JSON dari file drive_files.json
const dataPath = path.join(__dirname, "drive_files.json");
let driveFiles = [];
try {
  const fileData = fs.readFileSync(dataPath, "utf8");
  driveFiles = JSON.parse(fileData);
} catch (error) {
  console.error("Gagal membaca atau parsing drive_files.json:", error);
  process.exit(1);
}

// Set up Fuse.js untuk pencarian fuzzy pada field fileoriname
const fuseOptions = {
  keys: ["fileoriname"],
  threshold: 0.2, // atur threshold sesuai kebutuhan (0.0: ketat, 1.0: longgar)
};
const fuse = new Fuse(driveFiles, fuseOptions);

// Endpoint untuk mencari file berdasarkan judul (query parameter "title")
app.get("/search", (req, res) => {
  const query = req.query.title;
  if (!query) {
    return res.status(400).json({ error: "Parameter 'title' wajib diisi." });
  }

  const results = fuse.search(query);

  if (results.length === 0) {
    return res
      .status(404)
      .json({ error: "Tidak ada file yang cocok ditemukan." });
  }

  // Ambil hasil terbaik (paling relevan)
  const bestMatch = results[0].item;
  // Buat link berdasarkan filename dan base URL
  const link = `${BASE_URL}${bestMatch.filename}`;

  return res.json({
    filename: bestMatch.filename,
    fileid: bestMatch.fileid,
    fileoriname: bestMatch.fileoriname,
    link: link,
  });
});

// Jalankan server
app.listen(PORT, () => {
  console.log(`Server API berjalan di port ${PORT}`);
});
