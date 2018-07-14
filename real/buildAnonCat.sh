cut -f 1 data.txt | grep -v '^$' | sort -u | awk '{printf("%s\t%03d\n", $0, NR)}' > labels.tsv
