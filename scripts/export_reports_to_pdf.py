from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORD_REPORTS_DIR = ROOT / "deliverables" / "word-reports"
FINAL_DIR = ROOT / "deliverables" / "final-submission"


def export_docx_to_pdf(docx_path: Path, pdf_path: Path) -> None:
    script = f'''
set inputFile to POSIX file "{docx_path}"
set outputFile to POSIX file "{pdf_path}"
tell application "Pages"
    activate
    set theDoc to open inputFile
    export theDoc to outputFile as PDF
    close theDoc saving no
end tell
'''
    subprocess.run(["osascript", "-e", script], check=True)


def iter_report_roots() -> list[Path]:
    roots = [WORD_REPORTS_DIR]
    if FINAL_DIR.exists():
        for candidate in sorted(FINAL_DIR.iterdir()):
            if candidate.is_dir() and (candidate / "docx").exists():
                roots.append(candidate)
    return roots


def export_package(base_dir: Path) -> list[Path]:
    docx_dir = base_dir / "docx"
    pdf_dir = base_dir / "pdf"
    pdf_dir.mkdir(parents=True, exist_ok=True)
    exported: list[Path] = []
    for docx_path in sorted(docx_dir.glob("*.docx")):
        pdf_path = pdf_dir / (docx_path.stem + ".pdf")
        export_docx_to_pdf(docx_path, pdf_path)
        exported.append(pdf_path)
    return exported


def main() -> None:
    roots = [Path(arg).resolve() for arg in sys.argv[1:]] or iter_report_roots()
    for base_dir in roots:
        for pdf_path in export_package(base_dir):
            print(pdf_path.relative_to(ROOT))


if __name__ == "__main__":
    main()
