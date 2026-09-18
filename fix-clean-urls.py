#!/usr/bin/env python3
"""
Run this from the ROOT of your cloned repo (where index.html and the CNAME file live).

Converts every internal href="...index.html" (and canonical/link tags) back to
clean directory-style URLs, e.g.:
    href="analytics/index.html"        -> href="analytics/"
    href="../../index.html"            -> href="../../"
    href="index.html"                  -> href="./"
    href="index.html#respond"          -> href="#respond"
    href="../../index.html#respond"    -> href="../../#respond"

Safe on GitHub Pages / any real web server, since those auto-serve index.html
for a directory request. Do NOT run this if you're going back to viewing the
files via file:// or a plain static server with no directory-index support.
"""
import os
import re

ROOT = "."  # run from repo root

PATTERN = re.compile(r'(href|src)="((?:\.\./)*(?:[^"]*/)?)index\.html(#[^"]*)?"')

def repl(m):
    attr, prefix, anchor = m.group(1), m.group(2), m.group(3) or ""
    if anchor:
        # same-page anchor: drop the filename, keep just the fragment
        if prefix:
            return f'{attr}="{prefix}{anchor}"'
        return f'{attr}="{anchor}"'
    if prefix == "":
        return f'{attr}="./"'
    return f'{attr}="{prefix}"'

changed_files = 0
total_subs = 0

for dirpath, _, filenames in os.walk(ROOT):
    if ".git" in dirpath:
        continue
    for fn in filenames:
        if not fn.endswith(".html"):
            continue
        path = os.path.join(dirpath, fn)
        html = open(path, encoding="utf-8", errors="ignore").read()
        new_html, n = PATTERN.subn(repl, html)
        if n:
            open(path, "w", encoding="utf-8").write(new_html)
            changed_files += 1
            total_subs += n

print(f"Files changed: {changed_files}")
print(f"Links converted: {total_subs}")
print("Now run: git add -A && git commit -m 'Clean URLs for real web-server hosting' && git push")
