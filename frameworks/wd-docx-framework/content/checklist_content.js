/**
 * checklist_content.js
 * The MAK4I pre-public-repo checklist, expressed as a framework
 * content file so it's generated through the reusable framework
 * rather than a one-off script.
 */

const { heading, paragraph, note } = require("../lib/helpers");
const { HeadingLevel, Paragraph, TextRun, CheckBox } = require("docx");

function taskItem(text) {
  return new Paragraph({
    children: [new CheckBox({ checked: false }), new TextRun({ text: "  " + text })],
    spacing: { after: 100 },
    indent: { left: 360 },
  });
}

module.exports = {
  title: "MAK4I — Pre-Public-Repo Checklist",
  subtitle: "Tasks to complete before flipping the mak4i-protocol repo from private to public.",
  body: [
    heading("Blocking — do these before flipping to public", HeadingLevel.HEADING_1),
    taskItem(
      "Add a LICENSE file (MIT) to the repo root. Confirmed missing — every doc claims MIT licensing, but no LICENSE file currently exists."
    ),
    taskItem(
      "Re-read CONTRIBUTING.md's actual text and confirm it doesn't promise tooling that doesn't exist (a CLA process, specific issue/PR templates, a Discord/Slack, a mailing list)."
    ),
    taskItem(
      "Add basic .github/ISSUE_TEMPLATE and PULL_REQUEST_TEMPLATE.md if CONTRIBUTING.md references a contribution process. Confirmed no .github/ directory currently exists."
    ),
    taskItem(
      'Add a prominent "This is Phase 0" framing line near the top of README so visitors don\'t assume more is built than actually is (no code yet — correct per the roadmap, but should be stated plainly on arrival).'
    ),
    taskItem(
      'Do one final full-repo read for any remaining "production," "in production," "currently used by," or "measured" language beyond what an automated grep already caught.'
    ),

    heading("Worth checking — likely fine but unverified", HeadingLevel.HEADING_1),
    taskItem(
      "Confirm all internal cross-file links actually resolve on GitHub, not just locally — especially anchor links (#heading), since GitHub auto-generates heading slugs differently than a local render."
    ),
    taskItem(
      "Validate every artifact JSON file is valid JSON and matches the MAK-0001 schema it claims to follow."
    ),
    taskItem(
      "Review docs-framework/content — unclear if this is real public-facing content or internal scratch material that should be excluded."
    ),
    taskItem(
      "Check .gitignore — confirm nothing accidentally trackable (local env files, credentials, personal notes) got mixed in during editing sessions."
    ),

    heading("Not blocking, but a real decision either way", HeadingLevel.HEADING_1),
    taskItem(
      "Decide the actual GitHub repo ownership — personal account vs. the Talvik GitHub org, now that Talvik Inc. is incorporated."
    ),
    taskItem(
      "Confirm trademark status is described accurately anywhere the repo mentions it, since Talvik and MAK4I trademarks have now been filed."
    ),

    heading("Notes", HeadingLevel.HEADING_1),
    note(
      "Generated using frameworks/wd-docx-framework. Talvik Inc. is incorporated (Delaware); Talvik and MAK4I trademarks have been filed. Phase 2 (backend/API) has not started — this checklist covers documentation and repo hygiene only."
    ),
  ],
};
