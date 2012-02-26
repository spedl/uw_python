import urllib2
import re, os


index = 'index.html'
site_base = 'http://jon-jacky.github.com/uw_python/winter_2012/'
website = site_base + index
page = urllib2.urlopen(website).read()
output_file = "downloader_output.txt"

# I would like to add a line to remove the output file before adding more to it

# This is going to pull out all the links matching this format and return them
# in a list.
py_links = re.findall(r'<a href=(.*?\.py")>',page)


# Used for testing
#for link in py_links:
#    print link

# An alternative to stepping through would be to put all the links into one
# long string separated by spaces. Then the program can make one curl call and
# curl will process the links sequentially (if I read the man page correctly)
for link in py_links:
    if (link[1:5] == site_base[:4]):
        full_site = link
    else:
        full_site = site_base + link

    command = 'curl ' + full_site + ' --create-dirs -a -o %s' % output_file
    download = os.popen(command).read()
