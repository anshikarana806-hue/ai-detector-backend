import sharp from "sharp";

async function detectAI(file) {
  if (!file) {
    return {
      aiGenerated: false,
      confidence: "0%",
      reasons: ["No file received"]
    };
  }

  const reasons = [];
  let score = 0;

  // Load image
  const image = sharp(file.buffer);
  const metadata = await image.metadata();

  const width = metadata.width || 0;
  const height = metadata.height || 0;
  const pixels = width * height;
  const sizeKB = file.size / 1024;

  /* ---------- LOGIC 1: File size vs resolution ---------- */
  const bytesPerPixel = file.size / pixels;

  if (bytesPerPixel < 0.8) {
    reasons.push("Very low bytes-per-pixel (over-compressed or AI-generated)");
    score += 30;
  } else if (bytesPerPixel > 2.5) {
    reasons.push("High bytes-per-pixel (natural camera image)");
    score -= 10;
  }

  /* ---------- LOGIC 2: Format bias ---------- */
  if (file.mimetype === "image/png") {
    reasons.push("PNG format commonly used by AI generators");
    score += 15;
  }

  if (file.mimetype === "image/jpeg") {
    reasons.push("JPEG camera compression detected");
    score -= 5;
  }

  /* ---------- LOGIC 3: Color variance (entropy proxy) ---------- */
  const stats = await image.stats();
  const channelStd = stats.channels.map(c => c.stdev);
  const avgStd = channelStd.reduce((a, b) => a + b, 0) / channelStd.length;

  if (avgStd < 20) {
    reasons.push("Low color variance (over-smooth textures)");
    score += 25;
  } else {
    reasons.push("Natural color variance detected");
    score -= 10;
  }

  /* ---------- LOGIC 4: Resolution pattern ---------- */
  if (width === height && width >= 512 && width <= 2048) {
    reasons.push("Square resolution common in AI-generated images");
    score += 10;
  }

  /* ---------- FINAL DECISION ---------- */
  let aiGenerated = score >= 40;
  let confidence = Math.min(Math.max(score + 30, 10), 95);

  if (!aiGenerated) {
    reasons.push("Image characteristics align with natural photography");
  }

  return {
    aiGenerated,
    confidence: confidence + "%",
    reasons
  };
}

export { detectAI };

