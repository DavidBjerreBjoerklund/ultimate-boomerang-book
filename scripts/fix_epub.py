#!/usr/bin/env python3
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path


EMPTY_TITLE_RE = re.compile(r"<title>\s*</title>")
EMPTY_OL_RE = re.compile(r"<ol>\s*</ol>")
NAV_NUMBER_RE = re.compile(r"(<li>)\s*<span>[^<]+</span>[\s\u00a0]*(<a\b)")
LEADING_NAV_TEXT_RE = re.compile(r"(<li>)([^<]+?)(\s*<a\b)")


def fix_xhtml(path):
    text = path.read_text(encoding="utf-8")
    original = text
    text = EMPTY_TITLE_RE.sub("<title>The Ultimate Boomerang Book</title>", text)

    previous = None
    while previous != text:
        previous = text
        text = EMPTY_OL_RE.sub("", text)
    text = NAV_NUMBER_RE.sub(r"\1\2", text)
    text = LEADING_NAV_TEXT_RE.sub(lambda m: f"{m.group(1)}<span>{m.group(2).strip()}</span>{m.group(3)}", text)

    if text != original:
        path.write_text(text, encoding="utf-8")


def repack(source, workdir):
    with zipfile.ZipFile(source, "w") as epub:
        mimetype = workdir / "mimetype"
        epub.write(mimetype, "mimetype", compress_type=zipfile.ZIP_STORED)
        for path in sorted(workdir.rglob("*")):
            if path.is_dir() or path == mimetype:
                continue
            epub.write(path, path.relative_to(workdir).as_posix(), compress_type=zipfile.ZIP_DEFLATED)


def main():
    if len(sys.argv) != 2:
        print("Usage: fix_epub.py path/to/book.epub", file=sys.stderr)
        return 2

    epub_path = Path(sys.argv[1])
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        with zipfile.ZipFile(epub_path) as epub:
            epub.extractall(workdir)

        for xhtml in workdir.rglob("*.xhtml"):
            fix_xhtml(xhtml)

        tmp_epub = epub_path.with_suffix(".fixed.epub")
        repack(tmp_epub, workdir)
        shutil.move(tmp_epub, epub_path)

    print("EPUB normalization complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
