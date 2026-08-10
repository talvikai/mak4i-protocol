/**
 * tables.js
 * Builds a styled docx.js Table from a simple headers[] + rows[][]
 * input, so content files never construct Table/TableRow/TableCell
 * objects by hand.
 */

const { Table, TableRow, TableCell, Paragraph, TextRun, WidthType, ShadingType } = require("docx");
const styles = require("./styles");

/**
 * @param {string[]} headers
 * @param {string[][]} rows
 * @param {object} opts - { widths?: number[] } column widths in DXA (optional)
 */
function simpleTable(headers, rows, opts = {}) {
  const headerRow = new TableRow({
    tableHeader: true,
    children: headers.map(
      (h, i) =>
        new TableCell({
          width: opts.widths ? { size: opts.widths[i], type: WidthType.DXA } : undefined,
          shading: { type: ShadingType.CLEAR, fill: styles.colors.tableHeaderBg },
          children: [
            new Paragraph({
              children: [
                new TextRun({ text: h, bold: true, color: styles.colors.tableHeaderText }),
              ],
            }),
          ],
        })
    ),
  });

  const bodyRows = rows.map(
    (row, rowIndex) =>
      new TableRow({
        children: row.map(
          (cell, i) =>
            new TableCell({
              width: opts.widths ? { size: opts.widths[i], type: WidthType.DXA } : undefined,
              shading:
                rowIndex % 2 === 1
                  ? { type: ShadingType.CLEAR, fill: styles.colors.tableRowAltBg }
                  : undefined,
              children: [new Paragraph({ children: [new TextRun({ text: String(cell) })] })],
            })
        ),
      })
  );

  return new Table({
    rows: [headerRow, ...bodyRows],
    width: { size: 100, type: WidthType.PERCENTAGE },
  });
}

module.exports = { simpleTable };
