TEX = UBB.tex
LATEXMK = latexmk

.PHONY: build watch clean open

build:
	$(LATEXMK) -pdf -interaction=nonstopmode -synctex=1 $(TEX)

watch:
	$(LATEXMK) -pdf -pvc -interaction=nonstopmode -synctex=1 $(TEX)

clean:
	$(LATEXMK) -c $(TEX)

open:
	open UBB.pdf
