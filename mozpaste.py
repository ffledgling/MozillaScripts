# Pastebin Script for use with pastebin.mozilla.org
#
# In-Tree version available here:
# https://github.com/mozilla/mozilla-central/blob/master/tools/mach_commands.py

#!/usr/bin/python

import os
import argparse
import sys
import urllib
import urllib2

def pastebin(args):
    URL = 'http://pastebin.mozilla.org/'

    FILE_TYPES = [{'value': 'text', 'name': 'None', 'extension': 'txt' },
    {'value': 'bash', 'name': 'Bash', 'extension': 'sh' },
    {'value': 'c', 'name': 'C', 'extension': 'c' },
    {'value': 'cpp', 'name': 'C++', 'extension': 'cpp' },
    {'value': 'diff', 'name': 'Diff', 'extension': 'diff' },
    {'value': 'diff', 'name': 'Patch', 'extension': 'patch' },
    {'value': 'html4strict', 'name': 'HTML', 'extension': 'html' },
    {'value': 'javascript', 'name': 'Javascript', 'extension': 'js' },
    {'value': 'javascript', 'name': 'Javascript', 'extension': 'jsm' },
    {'value': 'lua', 'name': 'Lua', 'extension': 'lua' },
    {'value': 'perl', 'name': 'Perl', 'extension': 'pl' },
    {'value': 'php', 'name': 'PHP', 'extension': 'php' },
    {'value': 'python', 'name': 'Python', 'extension': 'py' },
    {'value': 'ruby', 'name': 'Ruby', 'extension': 'rb' },
    {'value': 'css', 'name': 'CSS', 'extension': 'css' },
    {'value': 'diff', 'name': 'Diff', 'extension': 'diff' },
    {'value': 'ini', 'name': 'INI file', 'extension': 'ini' },
    {'value': 'java', 'name': 'Java', 'extension': 'java' },
    {'value': 'xml', 'name': 'XML', 'extension': 'xml' },
    {'value': 'xml', 'name': 'XML', 'extension': 'xml' }]

    lang = ''
    poster = args.poster

    if args.file:
        try:
            with open(args.file, 'r') as f:
                content = f.read()
            # TODO: Use mime-types instead of extensions; suprocess('file <f_name>')
            # Guess File-type based on file extension
            extension = args.file.split('.')[-1]
            for l in FILE_TYPES:
                if extension == l['extension']:
                    print("Identified file as %s" % l['name'])
                    lang = l['value']
        except IOError:
            sys.stderr.write("Error: No such file\n")
            return 1
    else:
        content = sys.stdin.read()
    duration = args.duration[0]

    if args.language:
        lang = args.language


    params = [
        ('parent_pid', ''),
        ('format', lang),
        ('code2', content),
        ('poster', poster),
        ('expiry', duration),
        ('paste', 'Send')]

    data = urllib.urlencode(params)
    print("Uploading ...")
    try:
        req = urllib2.Request(URL, data)
        response = urllib2.urlopen(req)
        resp_code = response.getcode()
        if resp_code == 200:
            print(response.geturl())
        else:
            sys.stderr.write("Error: Could not upload file. HTTP Response Code %s\n" % resp_code)
            return 1
    except urllib2.URLError:
        sys.stderr.write("Error: Could not connect to pastebin.mozilla.org\n")
        return 1
    return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Commandline pastebin tool for use with pastebin.mozilla.org")

    parser.add_argument("-l", "--language",
                        help="Language to use for syntax highlighting",
                        default=None)

    parser.add_argument("--poster",
                        help="Specify your name for use with pastebin.mozilla.org",
                        default=None)
    parser.add_argument("--duration",
                        help="Keep for specified duration (default: %(default)s)",
                        default="day", choices=["d", "day", "m", "month", "f", "forever"])
    parser.add_argument("file", nargs="?",
                        help="Specify the file to upload to pastebin.mozilla.org",
                        default=None)

    args = parser.parse_args()

    pastebin(args)

