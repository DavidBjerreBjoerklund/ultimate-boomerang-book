TEX = UBB.tex
LATEXMK = latexmk

ifneq ($(wildcard /Library/TeX/texbin),)
PATH := /Library/TeX/texbin:$(PATH)
endif

ifeq ($(wildcard /Library/TeX/texbin/latexmk),/Library/TeX/texbin/latexmk)
LATEXMK = /Library/TeX/texbin/latexmk
endif

.PHONY: build watch clean open

build:
	$(LATEXMK) -pdf -interaction=nonstopmode -synctex=1 $(TEX)

watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode -synctex=1 $(TEX)

clean:
	$(LATEXMK) -c $(TEX)

open:
	open UBB.pdf
