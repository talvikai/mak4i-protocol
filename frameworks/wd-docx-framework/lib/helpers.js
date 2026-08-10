/**
 * helpers.js
 * Low-level building blocks for constructing a docx.js Document.
 * Every content file (content/*.js) composes documents using these
 * helpers rather than calling docx.js primitives directly, so styling
 * stays consistent across every generated document.
 */

const { Paragraph, TextRun, HeadingLevel, AlignmentType } = require("docx");
const styles = require("./styles");

function heading(text, level = HeadingLevel.HEADING_1) {
  return new Paragraph({
    text,
    heading: level,
    spacing: { before: styles.spacing.beforeHeading, after: styles.spacing.afterHeading },
  });
}

function paragraph(text, opts = {}) {
  return new Paragraph({
    children: [
      new TextRun({
        text,
        bold: opts.bold || false,
        italics: opts.italics || false,
        color: opts.color || styles.colors.body,
        size: opts.size || styles.fontSize.body,
      }),
    ],
    spacing: { after: opts.spacingAfter ?? styles.spacing.afterParagraph },
    alignment: opts.align || AlignmentType.LEFT,
    indent: opts.indent,
  });
}

function bulletItem(text, opts = {}) {
  return new Paragraph({
    children: [new TextRun({ text })],
    bullet: { level: opts.level || 0 },
    spacing: { after: styles.spacing.afterBullet },
  });
}

function note(text) {
  return paragraph(text, { italics: true, color: styles.colors.muted, size: styles.fontSize.small });
}

function titleBlock(title, subtitle) {
  const blocks = [
    new Paragraph({
      children: [new TextRun({ text: title, bold: true, size: styles.fontSize.title })],
      spacing: { after: 100 },
    }),
  ];
  if (subtitle) {
    blocks.push(
      new Paragraph({
        children: [new TextRun({ text: subtitle, italics: true, color: styles.colors.muted })],
        spacing: { after: 400 },
      })
    );
  }
  return blocks;
}

module.exports = {
  heading,
  paragraph,
  bulletItem,
  note,
  titleBlock,
};
