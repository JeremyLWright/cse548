proposal.pdf: proposal.tex References/References.bib
	pdflatex proposal
	biber proposal
	pdflatex proposal
	pdflatex proposal
	pdflatex proposal

clean:
	rm -rf *.bcf *.out *.aux *.bbl *.log *.run.xml *.blg

distclean: clean
	rm -rf *.pdf
