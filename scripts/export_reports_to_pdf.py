from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOCX_DIR = ROOT / "deliverables" / "word-reports" / "docx"
PDF_DIR = ROOT / "deliverables" / "word-reports" / "pdf"


def export_docx_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    script = f'''
tell application "Pages"
    activate
    set theDoc to open POSIX file "{docx_path}"
    export theDoc to POSIX file "{pdf_path}" as PDF
    close theDoc saving no
end tell
'''
    subprocess.run(["osascript", "-e", script], check=True)


def main() -> None:
    PDF_DIR.mkdir(parents=True, exist_ok=True)
    for docx_path in sorted(DOCX_DIR.glob("*.docx")):
        pdf_path = PDF_DIR / (docx_path.stem + ".pdf")
        export_docx_to_pdf(docx_path, pdf_path)
        print(pdf_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
