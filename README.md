# The Ultimate Boomerang Book

Source files and artwork for the 2026 open source edition of *The Ultimate Boomerang Book*.

The main LaTeX entry point is `UBB.tex`, with chapter content in `tex/` and artwork in `Pictures/` and `Planer/`.

## Build

Use `make build` from the repository root:

```sh
make build
```

Build the EPUB3 edition with:

```sh
make epub
```

The EPUB build generates PNG assets from the EPS/PDF figure sources, builds `build/epub/UBB.epub`, and checks that packaged images and internal chapter/figure/section references resolve.

## Local Setup

macOS:

```sh
brew install --cask mactex-no-gui
```

Linux:

```sh
sudo apt-get update
sudo apt-get install -y latexmk texlive-latex-extra
```

Windows:

```powershell
choco install miktex -y
```

## GitHub

A GitHub Actions workflow builds the book on Linux and Windows so we catch platform issues early.
