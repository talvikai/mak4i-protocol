/**
 * template.js
 * Takes a content definition (see content/example_content.js for the
 * expected shape) and assembles it into a complete docx.js Document.
 * This is the layer content files are written against — they describe
 * *what* goes in the document, this module handles *how* it becomes
 * a valid Document object.
 */

const { Document } = require("docx");
const { titleBlock } = require("./helpers");

/**
 * @param {object} contentDef
 * @param {string} contentDef.title
 * @param {string} [contentDef.subtitle]
 * @param {(import("docx").Paragraph|import("docx").Table)[]} contentDef.body
 *   An array of already-built Paragraph/Table elements, typically
 *   produced using helpers.js and tables.js in the content file.
 */
function buildDocument(contentDef) {
  if (!contentDef || !Array.isArray(contentDef.body)) {
    throw new Error(
      "Content definition must export { title, subtitle?, body: [...] } — body must be an array of docx elements."
    );
  }

  const children = [...titleBlock(contentDef.title, contentDef.subtitle), ...contentDef.body];

  return new Document({
    sections: [{ children }],
  });
}

module.exports = { buildDocument };
