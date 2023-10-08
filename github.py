#!/usr/bin/env python3
import os
import sys
import re
from os.path import exists
import requests
import time

token = os.environ.get("GITHUB_TOKEN")
output_file = "githubregexes.txt"

if token is None:
    print("No GITHUB_TOKEN")
    sys.exit()

re_re = re.compile("""(?:re\.)?[matchfindallitersearch]*\((?P<quote>['"])(?P<regex>.*?)(?P=quote)""")

codesearch_url = 'https://api.github.com/search/code'
search_term = "re.{}(' language:python in:file"

regexes = set([])

#load regexes from previous runs
if exists(output_file):
    with open(output_file,"r",encoding="utf-8") as fid:
        for regex in fid:
            regexes.add(regex[:-1])

print("Before:",len(regexes))

for func in ["match","search","findall"]:
    print("Finding {func} occurences")
    for i in range(1,11):
        params = dict(per_page=100,
                      page=i,
                      q=search_term.format(func))
        headers = dict(Accept="application/vnd.github.v3.text-match+json",
                       Authorization=f"Bearer {token}")
        r = requests.get(codesearch_url,params=params,headers=headers)

        if r.ok:
            print("processing page of results")
            for ri in r.json()["items"]:
                for m in ri["text_matches"]:
                    for match in re.finditer(re_re,m["fragment"]):
                        regexes.add(match.group("regex"))
        else:
            print("request failed: {}", r)

        time.sleep(10)

print("After",len(regexes))

with open(output_file,"w", encoding="utf-8") as fid:
    for regex in regexes:
        fid.write(f"{regex}\n")
