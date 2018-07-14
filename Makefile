
simulation/rating.tsv: simulation/ratings.py
	python simulation/ratings.py > simulation/ratings.tsv

dot.pdf: simulation/ratings.py
	python simulation/ratings.py

