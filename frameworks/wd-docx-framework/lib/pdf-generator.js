/**
 * pdf-generator.js
 * Converts a .docx file to .pdf using headless LibreOffice, which is
 * the tool confirmed available in this environment (`soffice`).
 * Kept as a separate, optional step — docx generation succeeds
 * independently of whether PDF conversion is requested or available.
 */

const { execFileSync } = require("child_process");
const path = require("path");

/**
 * @param {string} docxPath - absolute or relative path to a .docx file
 * @param {string} outputDir - directory to write the resulting .pdf into
 * @returns {string} path to the generated .pdf file
 */
function convertToPdf(docxPath, outputDir) {
  try {
    execFileSync(
      "soffice",
      ["--headless", "--convert-to", "pdf", "--outdir", outputDir, docxPath],
      { stdio: "pipe" }
    );
  } catch (err) {
    throw new Error(
      `PDF conversion failed. Ensure LibreOffice (soffice) is installed and on PATH.\nOriginal error: ${err.message}`
    );
  }

  const base = path.basename(docxPath, path.extname(docxPath));
  return path.join(outputDir, `${base}.pdf`);
}

module.exports = { convertToPdf };
