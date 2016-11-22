import requests
import re
from codecs import open
import getpass
from os.path import exists

username = raw_input("Username:")
password = getpass.getpass("Password:")

output_file = "githubregexes.txt"

re_re = re.compile("""(?:re\.)?[matchfindallitersearch]*\((?P<quote>['"])(?P<regex>.*?)(?P=quote)""")

codesearch_url = 'https://api.github.com/search/code'
search_term = "re.{}(' language:python in:file"

regexes = set([])

#load regexes from previous runs
if exists(output_file):
    with open(output_file,"r","utf8") as fid:
        for regex in fid:
            regexes.add(regex[:-1])

print "Before:",len(regexes)

for func in ["match","search","findall"]:
    for i in range(1,11):
        params = dict(per_page=100,
                      page=i,
                      q=search_term.format(func))
        auth=(username,password)
        headers = dict(Accept="application/vnd.github.v3.text-match+json")
        r = requests.get(codesearch_url,params=params,headers=headers,auth=auth)

        if r.ok:
            for r in r.json()["items"]:
                for m in r["text_matches"]:
                    for match in re.finditer(re_re,m["fragment"]):
                        regexes.add(match.group("regex"))

print "After",len(regexes)

with open(output_file,"w","utf8") as fid:
    for regex in regexes:
        fid.write(u"{}\n".format(regex))

