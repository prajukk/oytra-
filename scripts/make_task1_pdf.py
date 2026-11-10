from fpdf import FPDF
from pathlib import Path
import textwrap

out = Path(r"d:\odee\oytra\oytra-\task1\Task1_QA_Report_Praju.pdf")


class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def safe(text: str) -> str:
    return (
        text.replace("\u2014", "-")
        .replace("\u2013", "-")
        .replace("\u2019", "'")
        .replace("\u201c", '"')
        .replace("\u201d", '"')
        .encode("latin-1", "replace")
        .decode("latin-1")
    )


def write_wrapped(pdf: FPDF, text: str, size=11, style="", line_h=6):
    pdf.set_font("Helvetica", style, size)
    pdf.set_x(pdf.l_margin)
    width = pdf.epw
    # Force break long tokens (URLs)
    pieces = []
    for word in text.split(" "):
        if len(word) > 70:
            pieces.extend(textwrap.wrap(word, 70))
        else:
            pieces.append(word)
    wrapped = textwrap.fill(" ".join(pieces), width=95)
    for line in wrapped.splitlines() or [""]:
        pdf.set_x(pdf.l_margin)
        pdf.cell(width, line_h, safe(line), new_x="LMARGIN", new_y="NEXT")


pdf = PDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()
pdf.set_left_margin(15)
pdf.set_right_margin(15)

write_wrapped(pdf, "Task 1 - QA & Debug Report", size=16, style="B", line_h=9)
pdf.ln(3)

for line in [
    "App under test: Conduit (RealWorld) - https://demo.realworld.show/",
    "Also checked: https://demo.realworld.io/ (assignment-listed demo URL)",
    "Tester: Praju",
    "Date: 10 Nov 2026",
    "Scope: Home feed, Sign up, Sign in, New Article, Publish, Delete, Your Feed, Tags",
]:
    write_wrapped(pdf, line, size=11)

pdf.ln(2)
write_wrapped(
    pdf,
    "Note: demo.realworld.io currently returns 404 NoSuchBucket. Testing continued on the live Conduit demo at demo.realworld.show.",
    size=10,
    style="I",
)
pdf.ln(4)
write_wrapped(pdf, "Bug findings", size=13, style="B", line_h=8)
pdf.ln(2)

bugs = [
    (
        "1. Official RealWorld demo host is completely down [Critical]",
        "Steps: Open https://demo.realworld.io/",
        "Expected vs Actual: Expected Conduit demo loads. Actual AWS-style 404 NoSuchBucket for bucket demo.realworld.io.",
        "Suspected cause: Hosting misconfiguration / deleted S3 bucket or broken DNS-to-bucket mapping.",
    ),
    (
        "2. Delete Article has no confirmation [High]",
        "Steps: Sign in -> open your article -> click Delete Article",
        "Expected vs Actual: Expected confirm dialog before irreversible delete. Actual deletes immediately, no modal.",
        "Suspected cause: Delete handler calls API on click with no UX guard in the Angular article component.",
    ),
    (
        "3. Client-side validation is weak / bypassable [High]",
        "Steps: Register with email not-an-email and password 1. Also publish empty article.",
        "Expected vs Actual: Expected block invalid email/weak password/blank article client-side. Actual submit allowed; form novalidate; empty article only fails after API.",
        "Suspected cause: Incomplete reactive validators; HTML5 validation disabled via novalidate.",
    ),
    (
        "4. Document title never changes across routes [Medium]",
        "Steps: Visit /, /login, /register, /editor, article URL; check tab title.",
        "Expected vs Actual: Expected title reflects page. Actual always Conduit.",
        "Suspected cause: Angular Title service / route title metadata not configured.",
    ),
    (
        "5. Multiple H1 headings on feed and article pages [Medium]",
        "Steps: Open Global Feed; open article with markdown # Heading.",
        "Expected vs Actual: Expected one page-level H1. Actual feed card titles are H1; markdown also emits H1.",
        "Suspected cause: Semantic heading misuse + markdown renderer emits raw H1.",
    ),
    (
        "6. Forms lack accessible labels and live error regions [Medium]",
        "Steps: Inspect signup/signin/editor inputs and error list after failed submit.",
        "Expected vs Actual: Expected label[for] + role=alert/aria-live. Actual placeholders only; error list not announced.",
        "Suspected cause: Accessibility not implemented for forms.",
    ),
    (
        "7. Favorite control accessible name is only the count [Low]",
        "Steps: Inspect favorite buttons on Global Feed with a11y tree.",
        "Expected vs Actual: Expected Favorite article (1). Actual name is just 1 / 2.",
        "Suspected cause: Button text is only the favorites count; missing aria-label.",
    ),
]

for title, steps, expected, cause in bugs:
    write_wrapped(pdf, title, size=11, style="B")
    write_wrapped(pdf, steps, size=10)
    write_wrapped(pdf, expected, size=10)
    write_wrapped(pdf, cause, size=10)
    pdf.ln(3)

pdf.add_page()
write_wrapped(
    pdf,
    "Root-cause analysis (Issue #2 - Delete without confirmation)",
    size=13,
    style="B",
    line_h=8,
)
pdf.ln(3)
write_wrapped(
    pdf,
    "When an author clicks Delete Article, the UI immediately issues a DELETE request "
    "for that article slug and then navigates to Home. There is no intermediate confirmation "
    "step, so a mis-click permanently removes content. This almost certainly lives in the "
    "article detail component delete click handler: the button is wired directly to the "
    "articles API service (or store action) instead of opening a confirm dialog first. "
    "Because the demo also shows two Delete buttons (banner + footer), the accidental-click "
    "surface is doubled. Fix: (1) open a confirm modal with Cancel/Delete, (2) only call "
    "DELETE after affirmative action and disable buttons while in flight, (3) on failure keep "
    "the article page and show an error toast, (4) optionally soft-delete or add a short undo "
    "snackbar. This is a classic vibe-coded gap: the happy path works, but destructive "
    "actions lack production-grade guardrails.",
    size=11,
    line_h=6,
)
pdf.ln(4)
write_wrapped(pdf, "Evidence / notes", size=13, style="B", line_h=8)
pdf.ln(2)
write_wrapped(pdf, "Screenshots: screenshots/01-empty-article-validation-errors.png", size=11)
write_wrapped(pdf, "Screenshots: screenshots/02-official-demo-realworld-io-404.png", size=11)
write_wrapped(
    pdf,
    "Assumptions: session isolation may reset demo data; bugs reproduced 10 Nov 2026. "
    "XSS payloads in titles/bodies appeared escaped/stripped (positive finding).",
    size=11,
)

pdf.output(str(out))
print(f"wrote {out} ({out.stat().st_size} bytes)")
