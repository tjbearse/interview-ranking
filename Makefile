
simulation/rating.tsv: simulation/ratings.py
	python simulation/ratings.py > simulation/ratings.tsv

simulation/dot.png: simulation/ratings.py
	python simulation/ratings.py | dot -Tpng -o simulation/dot.png
	open simulation/dot.png

