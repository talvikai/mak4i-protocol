# WD DOCX Framework

Reusable Node.js framework for generating professional DOCX documents,
with optional PDF conversion. Built to eliminate rebuilding document
generation logic each session — write a content file, run one command,
get a formatted document.

Referenced by the [`wd-docx-framework`](../../artifacts/document/wd-docx-framework-v1.0.0.json)
MAK4I artifact. This directory is the actual, tested source — the
artifact JSON is its catalog entry.

## Usage

```bash
npm install
node run.js --format docx --content content/my_content.js
node run.js --format pdf  --content content/my_content.js
```

PDF conversion requires LibreOffice (`soffice`) installed and on PATH.

## Structure

```
wd-docx-framework/
├── run.js                    Entry point / CLI
├── lib/
│   ├── helpers.js            heading(), paragraph(), bulletItem(), note(), titleBlock()
│   ├── styles.js              Shared colors, spacing, font sizes
│   ├── tables.js              simpleTable(headers, rows)
│   ├── template.js            Assembles a content definition into a Document
│   └── pdf-generator.js       docx → pdf via headless LibreOffice
├── content/
│   ├── example_content.js     Working reference example
│   └── checklist_content.js   Real example — MAK4I pre-launch checklist
└── output/                    Generated files land here (gitignored)
```

## Writing a content file

A content file exports `{ title, subtitle?, body: [...] }`, where `body`
is an array of elements built using the helpers in `lib/helpers.js` and
`lib/tables.js`:

```js
const { heading, paragraph, bulletItem } = require("../lib/helpers");
const { simpleTable } = require("../lib/tables");
const { HeadingLevel } = require("docx");

module.exports = {
  title: "My Document",
  subtitle: "Optional subtitle",
  body: [
    heading("Section One", HeadingLevel.HEADING_1),
    paragraph("Some body text."),
    bulletItem("A bullet point"),
    simpleTable(["Col A", "Col B"], [["1", "2"], ["3", "4"]]),
  ],
};
```

See `content/example_content.js` for a complete, runnable example.

## Status

Tested end-to-end on 2026-08-07: docx generation and PDF conversion both
confirmed working (`content/example_content.js` and
`content/checklist_content.js`, both producing valid, structurally
correct output). This is a rebuild — the framework artifact predates
this session, and the original source was not available here; this
version was written fresh against the artifact's documented interface
and command signature (`node run.js --format docx --content
content/my_content.js`) so it matches what the artifact describes.

## License

MIT
