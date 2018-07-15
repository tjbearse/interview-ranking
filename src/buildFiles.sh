#!/bin/bash
set -ue
LABELS=labels.tsv
ANON=anon.tsv
if [ -f "$LABELS" ]; then
	rm -i "$LABELS"
fi
if [ -f "$ANON" ]; then
	rm -i "$ANON"
fi
cut -f 1 $1 | grep -v '^$' | sort -u | awk '{printf("%s\t%03d\n", $0, NR)}' > "$LABELS"
sed -f <( <"$LABELS" sed 's/^\([^\t]*\)\t\([[:digit:]]*\)$/s#^\1\t#\2\t#/') $1 > "$ANON"
