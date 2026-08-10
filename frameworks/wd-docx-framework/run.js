#!/usr/bin/env node
/**
 * run.js
 * Entry point for the WD DOCX Framework.
 *
 * Usage:
 *   node run.js --format docx --content content/my_content.js
 *   node run.js --format pdf  --content content/my_content.js
 *
 * A content file must export { title, subtitle?, body: [...] } —
 * see content/example_content.js for a working reference.
 */

const path = require("path");
const fs = require("fs");
const { Packer } = require("docx");
const { buildDocument } = require("./lib/template");
const { convertToPdf } = require("./lib/pdf-generator");

function parseArgs(argv) {
  const args = { format: "docx" };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--format") args.format = argv[++i];
    if (argv[i] === "--content") args.content = argv[++i];
    if (argv[i] === "--out") args.out = argv[++i];
  }
  return args;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (!args.content) {
    console.error(
      "Missing required --content argument.\nUsage: node run.js --format docx --content content/my_content.js"
    );
    process.exit(1);
  }

  const contentPath = path.resolve(process.cwd(), args.content);
  if (!fs.existsSync(contentPath)) {
    console.error(`Content file not found: ${contentPath}`);
    process.exit(1);
  }

  const contentDef = require(contentPath);
  const doc = buildDocument(contentDef);

  const outputDir = path.resolve(__dirname, "output");
  if (!fs.existsSync(outputDir)) fs.mkdirSync(outputDir, { recursive: true });

  const baseName = args.out || path.basename(contentPath, path.extname(contentPath));
  const docxPath = path.join(outputDir, `${baseName}.docx`);

  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(docxPath, buffer);
  console.log(`Wrote ${docxPath}`);

  if (args.format === "pdf") {
    const pdfPath = convertToPdf(docxPath, outputDir);
    console.log(`Wrote ${pdfPath}`);
  }
}

main().catch((err) => {
  console.error("Generation failed:", err.message);
  process.exit(1);
});
