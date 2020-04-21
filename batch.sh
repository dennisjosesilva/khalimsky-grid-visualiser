mkdir output
mkdir output/paper
mkdir output/paper/tikz
mkdir output/paper/pdf
mkdir output/paper/tikz/upper
mkdir output/paper/tikz/lower
mkdir output/paper/pdf/upper
mkdir output/paper/pdf/lower
# C image 
mkdir output/c 
mkdir output/c/tikz
mkdir output/c/pdf
mkdir output/c/tikz/upper
mkdir output/c/tikz/lower
mkdir output/c/pdf/upper
mkdir output/c/pdf/lower
#
# generate maps for paper.txt image
#
# interpolation
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/interpolation.pdf \
	--tex_output output/paper/tikz/interpolation.tex --step interpolation 
# immersion
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/immersion.pdf \
	--tex_output output/paper/tikz/immersion.tex --step immersion 
# depth 
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/depth.pdf \
	--tex_output output/paper/tikz/depth.tex --step depth
# upper level-sets
# value 0
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/upper/0.pdf \
	--tex_output output/paper/tikz/upper/0.tex --step thres_immersion_upper --thres_value 0
# value 4
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/upper/4.pdf \
	--tex_output output/paper/tikz/upper/4.tex --step thres_immersion_upper --thres_value 4
# value 7
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/upper/7.pdf \
	--tex_output output/paper/tikz/upper/7.tex --step thres_immersion_upper --thres_value 7
# lower level-sets
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/lower/0.pdf \
	--tex_output output/paper/tikz/lower/0.tex --step thres_immersion_lower --thres_value 0
# value 4
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/lower/4.pdf \
	--tex_output output/paper/tikz/lower/4.tex --step thres_immersion_lower --thres_value 4
# value 7
python3 main.py --pdflatex --input_image paper.txt --pdf_output output/paper/pdf/lower/7.pdf \
	--tex_output output/paper/tikz/lower/7.tex --step thres_immersion_lower --thres_value 7
#
# generate maps for c.txt image
#
# interpolation
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/interpolation.pdf \
	--tex_output output/c/tikz/interpolation.tex --step interpolation 
# immersion
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/immersion.pdf \
	--tex_output output/c/tikz/immersion.tex --step immersion 
# depth 
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/depth.pdf \
	--tex_output output/c/tikz/depth.tex --step depth
# upper level-sets
# value 0
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/upper/0.pdf \
	--tex_output output/c/tikz/upper/0.tex --step thres_immersion_upper --thres_value 0
# value 4
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/upper/1.pdf \
	--tex_output output/c/tikz/upper/1.tex --step thres_immersion_upper --thres_value 1
# value 7
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/upper/2.pdf \
	--tex_output output/c/tikz/upper/2.tex --step thres_immersion_upper --thres_value 2
# lower level-sets
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/lower/0.pdf \
	--tex_output output/c/tikz/lower/0.tex --step thres_immersion_lower --thres_value 0
# value 4
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/lower/1.pdf \
	--tex_output output/c/tikz/lower/1.tex --step thres_immersion_lower --thres_value 1
# value 7
python3 main.py --pdflatex --input_image c.txt --pdf_output output/c/pdf/lower/2.pdf \
	--tex_output output/c/tikz/lower/2.tex --step thres_immersion_lower --thres_value 2