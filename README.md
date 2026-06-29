# The Ultimate Boomerang Book

Source files and artwork for the 2026 open source edition of *The Ultimate Boomerang Book*.

The main LaTeX entry point is `UBB.tex`, with chapter content in `tex/` and artwork in `Pictures/` and `Planer/`.

## Build

Use `make build` from the repository root:

```sh
make build
```

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
