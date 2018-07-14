sed -f <(<labels.tsv sed 's/\([^\t]*\)\t\([[:digit:]]*\)/s#\1#\2#/') data.txt
