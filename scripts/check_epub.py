#!/usr/bin/env python3
import posixpath
import re
import sys
import zipfile
from html import unescape
from urllib.parse import unquote, urlsplit


ATTR_RE = re.compile(r"""\b(?P<attr>href|src)\s*=\s*['"](?P<value>[^'"]+)['"]""")
ID_RE = re.compile(r"""\b(?:id|name)\s*=\s*['"](?P<value>[^'"]+)['"]""")
CONTENT_SRC_RE = re.compile(r"""\bcontent\s+src\s*=\s*['"](?P<value>[^'"]+)['"]""")


def norm_join(base, target):
    return posixpath.normpath(posixpath.join(posixpath.dirname(base), target))


def is_external(value):
    scheme = urlsplit(value).scheme
    return scheme in {"http", "https", "mailto", "tel", "data"}


def collect_ids(files):
    ids = {}
    for name, text in files.items():
        ids[name] = {unescape(match.group("value")) for match in ID_RE.finditer(text)}
    return ids


def check(epub_path):
    errors = []
    with zipfile.ZipFile(epub_path) as epub:
        names = set(epub.namelist())
        text_files = {
            name: epub.read(name).decode("utf-8", "replace")
            for name in names
            if name.endswith((".xhtml", ".html", ".opf", ".ncx"))
        }
        ids_by_file = collect_ids(text_files)

        for name, text in text_files.items():
            matches = list(ATTR_RE.finditer(text))
            matches += list(CONTENT_SRC_RE.finditer(text))
            for match in matches:
                value = unescape(match.group("value"))
                if not value or is_external(value):
                    continue

                split = urlsplit(value)
                path = unquote(split.path)
                fragment = unquote(split.fragment)
                target_file = name if path == "" else norm_join(name, path)

                if path and target_file not in names:
                    errors.append(f"{name}: missing target file {value!r} -> {target_file}")
                    continue

                if fragment:
                    target_ids = ids_by_file.get(target_file, set())
                    if fragment not in target_ids:
                        errors.append(f"{name}: missing fragment {value!r} -> {target_file}#{fragment}")

    if errors:
        print(f"EPUB link check failed: {len(errors)} problem(s)", file=sys.stderr)
        for error in errors[:80]:
            print(f"- {error}", file=sys.stderr)
        if len(errors) > 80:
            print(f"... {len(errors) - 80} more", file=sys.stderr)
        return 1

    print("EPUB link check passed: all packaged image and internal reference targets exist.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: check_epub.py path/to/book.epub", file=sys.stderr)
        sys.exit(2)
    sys.exit(check(sys.argv[1]))
