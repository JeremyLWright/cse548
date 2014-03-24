inkscape -z -Acan_frame.pdf can_frame.svg
pdflatex -interaction=batchmode survey.tex
biber survey
pdflatex -interaction=batchmode survey.tex
pdflatex -interaction=batchmode survey.tex
pdflatex -interaction=batchmode survey.tex
