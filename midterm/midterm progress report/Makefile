proposal.pdf: proposal.tex References/References.bib machine.pdf job_file.pdf signalpath.pdf
	pdflatex proposal
	biber proposal
	pdflatex proposal
	pdflatex proposal
	pdflatex proposal

.SUFFIXES: .pdf.dot

machine.pdf: machine.dot
	dot -Tpdf machine.dot > machine.pdf

job_file.pdf: job_file.dot
	dot -Tpdf job_file.dot > job_file.pdf

signalpath.pdf: signalpath.dot
	dot -Tpdf signalpath.dot > signalpath.pdf

clean:
	rm -rf *.bcf *.out *.aux *.bbl *.log *.run.xml *.blg

distclean: clean
	rm -rf *.pdf
