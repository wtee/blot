#!/usr/bin/awk -f

# This is free and unencumbered software released into the public domain
# under the terms of the Unlicense <http://unlicense.org>.

# BLP -- a simple, somewhat Blosxom-like parser that treats the first 
# line of a page like a title to be made into a header and 
# assumes the the rest of the document is plain HTML. Written
# for use with the blot blogging script.

NR == 1 {print "<h4>" $0 "</h4>"}
NR > 1 {print}
