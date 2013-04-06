#!/bin/sh

# This is free and unencumbered software released into the public domain
# under the terms of the Unlicense <http://unlicense.org>.

# Configuration variables

# Where your files are
data_dir="blog"

# The title of your blog
title="My Blog"

# The CSS for your blog, if you have one
css_link="blot.css"

# The number of posts to show per page 
posts_per_page=6

# The program used to interepret your posts. If they're in plain HTML, just use '/bin/cat'
#parse="/bin/cat"
#parse="$(dirname ${path_to_files})/blp.awk"
parse="$(dirname ${path_to_files})/md2html.awk"

# The language your blog is in
lang="en-US"

# The character set you wrote your blog in
charset="UTF-8"

# END configuration variables. Please don't change things below unless you know what you're doing
# and/or feel dangerous.

blot_link="http://wt.gopherite.org/s/blot/"
version="blot 0.1 (I'm beta!)"

# Print all the header stuffs
/bin/echo "Content-type: text/html"
# I know it looks stupid to have a blank echo, but it's trailing newline is a functional, portable way of getting that
# much needed second line ending for the content header
/bin/echo
/bin/echo "<!doctype html><html lang=\"${lang}\"><head><meta charset=\"${charset}\"><meta name=\"viewport\" content=\"width=device width initial-scale=1\">"
/bin/echo "<title>${title}</title><link rel=\"stylesheet\" type=\"text/css\" href=\"${css_link}\" /></head><body>"
/bin/echo "<h1>${title}</h1>"

# Print the blog posts, etc.

# Print an individual post
if [ $QUERY_STRING != "" ]
then
  if [ -f ${data_dir}/${QUERY_STRING} ]
  then
    $parse ${data_dir}/${QUERY_STRING}
  # Print older post pages
  elif [ $(/bin/echo $QUERY_STRING | /usr/bin/sed s/[0-9]//g) = 'p=' ]
  then
    page_num=$(/bin/echo ${QUERY_STRING} | /usr/bin/sed s/[^0-9]//g)
    min=$((${page_num} * ${posts_per_page} + 1))
    max=$((${min} + ${posts_per_page} - 1))

    for f in $(/bin/ls -t -1 $data_dir | /usr/bin/awk -v mn="$min" -v mx="$max" 'NR >= mn && NR <= mx {print}')
    do
      date=$(/bin/ls -l -T ${data_dir}/${f} | /usr/bin/awk '{print $9 " " $7 " "  $6}')
      /bin/echo "<h3><a href=\"${SCRIPT_FILE_NAME}?${f}\">${date}</a></h3>"
      $parse ${data_dir}/$f
    done
    # If there are leftover posts, add a link to old posts
    if [ $(/bin/ls -1 ${data_dir} | /usr/bin/wc -l) -gt $(($posts_per_page + $posts_per_page * $page_num)) ]
    then
      /bin/echo "<p><a href=\"${SCRIPT_FILE_NAME}?p=$(($page_num + 1))\">Older posts</a></p>"
    fi
  else
    # Give an error message if the post doesn't exist
    /bin/echo "Sorry, this page does not seem to exist."
  fi
else
  # Print the default page
  for f in $(/bin/ls -t $data_dir | head -${posts_per_page})
  do
    date=$(/bin/ls -l -T ${data_dir}/${f} | /usr/bin/awk '{print $9 " " $7 " "  $6}')
    /bin/echo "<h3><a href=\"${SCRIPT_FILE_NAME}?${f}\">${date}</a></h3>"
    $parse ${data_dir}/$f
  done
  # If there are leftover posts, ad a link to old posts
  if [ $(/bin/ls -1 ${data_dir} | /usr/bin/wc -l) -gt $posts_per_page ]
  then
    /bin/echo "<p><a href=\"${SCRIPT_FILE_NAME}?p=1\">Older posts</a></p>"
  fi
fi

# End the document
# Comment this line out if you don't like free advertising. It's cool. I'd probably do it. 
/bin/echo "<p><a href=\"${blot_link}\">${version}</a></p>"

# Don't comment this line out. That'd be silly.
/bin/echo "</body></html>"
