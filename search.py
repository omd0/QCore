#!/usr/bin/env python

#*******************************************************************************
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# 
# ******************************************************************************/

import os
import string
from os import listdir
from os.path import basename, isdir, isfile, join
import re
import cgi
import sys

AND = "AND"
OR = "OR"
CASE_INSENSITIVE = "Insensitive"
CASE_SENSITIVE = "Sensitive"

# This is the base directory containg the files to
# search.  You will need to change this variable to
# point to the directory where your files will be
# found.
BASE_DIR = "test/"

# Python version 2.3 added the enumerate function.
# However, we might need to run on an older system
# so we created our own enumerate function
def enumeratez(seq):
    i = 0
    result = []
    for elem in seq:
        t = i, elem
        result.append(t)
        i += 1
    return result

# This function will parse the search terms.  It handles
# grouping the terms together if there are quotes and
# separating the single string of the terms into a tuple
# with each element containing a search term.
def parseTerms(terms):

    found = []

    buf = ""
    inquote = 0

    terms = terms.strip()

    for c in terms:
        if c == "\"":
            if inquote == 0:
                inquote = 1
            else:
                inquote = 0
                found.append(buf)
                buf = ""
            continue
        if c.isspace():
            if inquote == 0:
                if len(buf) > 0:
                    found.append(buf)
                    buf = ""
                continue
        buf += c

    if len(buf) > 0:
        found.append(buf)

    if inquote:
        raise NameError('Too many quotes')

    return found

# We don't want to find strings inside of HTML tags.  For example,
# if there is a tag which looks like <span class="blue"> we don't
# want to find the strings span, class, or blue.  The easiest and
# fastest way to do this is to remove all of the text inside of HTML
# tags.  The best way to do this is to parse the HTML and create a
# new buffer containing just the contents and not the tags.  However,
# parsing the file will be slow.  We will just do a quick and dirty
# search and remove all the tags ourselves.  It isn't perfect, but
# it isn't too bad.
#
# This method returns a string containing the text passed in with
# all of the HTML tags removed.
def remove_tags(in_text):
    # convert in_text to a mutable object (e.g. list)
    s_list = list(in_text)
    i,j = 0,0

    while i < len(s_list):
        # find the <
        if s_list[i] == '<':
            while s_list[i] != '>':
                # remove everything between the < and the >
                s_list.pop(i)

            # make sure we get rid of the > to
            s_list.pop(i)
        else:
            i=i+1

    join_char=''
    return join_char.join(s_list)

# This function will setup the parameters of the search and
# then call the dosearch function.
def search(terms, searchtype, case, files = []):
    return dosearch(parseTerms(terms), searchtype, case, "", files)

# This is the method which actually finds the search terms.
# This method returns 1 if the terms was found and -1 if
# it was not.
def dofind(line, case, searchtype, terms = []):
    if case == CASE_INSENSITIVE:
        line = line.lower()
        tmpterms = []
        for term in terms:
            tmpterms.append(term.lower())
        terms = tmpterms

    if searchtype == "AND":
        foundit = True
        for term in terms:
            if line.find(term) == -1:
                foundit = False
        if foundit:
            return 1
    else:
        for term in terms:
            if line.find(term) > 0:
                return 1

    return -1

# This method does the searching for the terms.  It also gets
# the title of each page where the search terms are found to
# use in the search results page.  This method will return
# a tuple containing the file title and the file path.
#
# Example:
#       File One, file1.html, File Two, file2.html
def dosearch(terms, searchtype, case, adddir, files = []):
    # If passed a list of files and a set of terms it will
    # return only the files that match the terms.  searchtype
    # should be either AND or OR

    found = []

    if files != None:
        titlesrch = re.compile('<title>.*</title>')
        for file in files:

            title = ""
            if isdir(BASE_DIR + adddir + file):
                # if the file is a directory then we want to
                # recurse into all the files in that directory
                searchitems = dosearch(terms, searchtype, case,
                adddir + file + "/", listdir(BASE_DIR + adddir + file))
                for i, result in enumeratez(searchitems):
                    if i % 2 == 1:
                        continue
                    found.append(searchitems[i])
                    found.append(adddir + file + "/" + searchitems[i + 1])
                continue

            # We only want to look in *.htm and *.html files.
            if not (file.lower().endswith("html") or file.lower().endswith("htm")):
                continue

            filecontents = open(BASE_DIR + adddir + file, 'r').read()

            # Find the title before we strip out the HTML tags
            titletmp = titlesrch.search(filecontents)
            if titletmp != None:
                title = filecontents.strip()[titletmp.start() + 7:titletmp.end() - 8]

            # Now that we have found the title we can remove all of the HTML
            # tags and remove any whitespace at the beginning and end of the
            # buffer.
            filecontents = remove_tags(filecontents)
            filecontents = filecontents.lstrip()
            filecontents = filecontents.rstrip()

            # Now that the buffer is prepared we can actually do the find.
            if dofind(filecontents, case, searchtype, terms) > 0:
                found.append(title)
                found.append(file)

    return found

# This method will print out the results page incorporating
# the results from the search operation.
def doresultspage(terms = [], results = []):
    for line in open("SearchResults.html", 'r'):
        if line.find("${SEARCH_RESULTS_GO_HERE}") != -1:
            doresults(terms, results)
        elif line.find("${SEARCH_TERMS_GO_HERE}") != -1:
            termindex = line.find("${SEARCH_TERMS_GO_HERE}")
            searchterms = "<span id=\"search_terms\">" + terms + "</span>\n"
            print(line.replace("${SEARCH_TERMS_GO_HERE}", searchterms))
        else:
            print(line)


# This method prints out just the results section of the results
# page.
def doresults(terms = [], results = []):
    print("<div id=\"search_results\">\n<ol>")
    if len(results) == 0:
        print("<h3>Your search did not return any results.</h3>")
    for i, file in enumeratez(results):
        if i % 2 == 1:
            continue
        print("<li><a href=\"test/" + results[i + 1] + "?search=true&term=" + terms.replace("\"", "%22") + "\">")

        print(results[i] + "</a>\n")
    print("</ol>\n</div>\n")


# Our scripts starts execution here.  Everything before this point has been
# function and variable declarations.


form = cgi.FieldStorage()
results = []
terms = ""

try:
    if form.has_key("terms"):
        terms = form.getvalue("terms")
        results = search(form.getvalue("terms"), form.getvalue("boolean"),
                         form.getvalue("case"), listdir(BASE_DIR))
    else:
        # This is a little bit of test code.  This will never be called
        # when you call this class within your browser.  You probably want
        # to remove this before putting this into production.
        terms = "red blue three"
        results = search("red blue three", OR, CASE_SENSITIVE, listdir(BASE_DIR))

    doresultspage(terms, results)
except NameError:
    print("There was an error understanding your search request.  Please press the back button and try again.")
except:
    print
    var = "Really Unexpected error:", sys.exc_info()[0]
