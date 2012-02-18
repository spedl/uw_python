import urllib2
import re


website = 'http://jon-jacky.github.com/uw_python/winter_2012/index.html'
page = urllib2.urlopen(website).read()

# This is going to pull out all the links matching this format
py_links = re.findall(r'<a href=(.*?\.py)">',page)

# Used for testing
#for link in py_links:
#    print link

# An alternative to stepping through would be to put all the links into one
# long string separated by spaces. Then the program can make one curl call and
# curl will process the links sequentially (if I read the man page correctly)
for link in py_links.group(): # or is it groups? 
    os.popen.('curl ' + link + ' --create-dirs -a -o "downloader_output.txt"').read()
