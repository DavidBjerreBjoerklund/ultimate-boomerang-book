TEX = UBB.tex
LATEXMK = latexmk
EPUB_DIR = build/epub
EPUB_BUILD_DIR = build/tex4ebook

ifneq ($(wildcard /Library/TeX/texbin),)
PATH := /Library/TeX/texbin:$(PATH)
endif

ifeq ($(wildcard /Library/TeX/texbin/latexmk),/Library/TeX/texbin/latexmk)
LATEXMK = /Library/TeX/texbin/latexmk
endif

.PHONY: build watch clean open epub epub-assets epub-check

build:
	$(LATEXMK) -pdf -interaction=nonstopmode -synctex=1 $(TEX)

epub-assets:
	./scripts/build_epub_assets.sh

epub: epub-assets
	mkdir -p $(EPUB_DIR) $(EPUB_BUILD_DIR)
	tex4ebook -f epub3 -c UBB.cfg -d $(EPUB_DIR) -B $(EPUB_BUILD_DIR) $(TEX)
	sleep 1
	python3 scripts/fix_epub.py $(EPUB_DIR)/UBB.epub
	python3 scripts/check_epub.py $(EPUB_DIR)/UBB.epub
	python3 scripts/fix_epub.py $(EPUB_DIR)/UBB.epub
	@if command -v epubcheck >/dev/null 2>&1; then epubcheck $(EPUB_DIR)/UBB.epub; else echo "epubcheck not found; skipped official EPUB validation."; fi

epub-check:
	python3 scripts/check_epub.py $(EPUB_DIR)/UBB.epub
	@if command -v epubcheck >/dev/null 2>&1; then epubcheck $(EPUB_DIR)/UBB.epub; else echo "epubcheck not found; skipped official EPUB validation."; fi

watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode -synctex=1 $(TEX)

clean:
	$(LATEXMK) -c $(TEX)

open:
	open UBB.pdf
