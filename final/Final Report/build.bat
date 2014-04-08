pdflatex proposal.tex
biber proposal
pdflatex proposal.tex
pdflatex proposal.tex
pdflatex proposal.tex
latexdiff --flatten ..\..\proposal\proposal.tex proposal.tex > diff.tex

pdflatex diff.tex
biber diff
pdflatex diff.tex
pdflatex diff.tex
pdflatex diff.tex

