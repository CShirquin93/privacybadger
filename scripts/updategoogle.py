#!/usr/bin/env python

import json
import sys

from collections import OrderedDict

def convert(text):
    patterns = list()
    for domain in text.split():
        patterns.append("https://www" + domain + "/*")
        patterns.append("http://www" + domain + "/*")
    return patterns

def update_manifest(supported_domains_path, manifest_path):
    with open(manifest_path, 'r') as f:
        manifest = json.load(f, object_pairs_hook=OrderedDict)

    with open(supported_domains_path, 'r+') as f:
        match_patterns = convert(f.read())

        scripts_idx = -1
        for idx, entry in enumerate(manifest['content_scripts']):
            if "js/firstparties/google-search.js" in entry['js']:
                scripts_idx = idx
                break
        if scripts_idx == -1:
            print("Failed to locate the Google Search content script in the manifest!")
            sys.exit(1)

        manifest['content_scripts'][scripts_idx]['matches'] = match_patterns

        f.seek(0)
        # print() auto-adds a trailing newline
        print(
            json.dumps(
                manifest,
                sort_keys=False,
                indent=2,
                separators=(',', ': ')
            ),
            file=f
        )
        f.truncate()

if __name__ == '__main__':
    # argv[1]: the path to a copy of https://www.google.com/supported_domains
    # argv[2]: the path to the extension manifest
    update_manifest(sys.argv[1], sys.argv[2])
