import urllib.request
import re
import json
# Load projects from a .json file
projects = json.loads(open("top-pypi-packages-30-days.min.json").read())
# Extract the project names in projects
project_names = [project["project"] for project in projects]

# Add standard library!
import sys
project_names.extend(list(sys.stdlib_module_names))
frozenset({"cProfile", "fractions", "_py_abc", "mailbox", "_typing", "fcntl", "antigravity", "_compression", "codecs", "pathlib", "_functools", "_pydecimal", "copy", "pickle", "urllib", "encodings", "netrc", "tempfile", "http", "_frozen_importlib", "sre_constants", "traceback", "sqlite3", "cmath", "codeop", "_osx_support", "_random", "_curses", "readline", "imaplib", "_posixshmem", "_scproxy", "collections", "dis", "doctest", "getpass", "_gdbm", "mmap", "xml", "code", "fileinput", "stat", "sched", "_curses_panel", "chunk", "asyncore", "_pyio", "_datetime", "weakref", "builtins", "uu", "mimetypes", "sre_compile", "functools", "zipfile", "_opcode", "socket", "_asyncio", "_hashlib", "timeit", "webbrowser", "_codecs_hk", "_codecs_jp", "_pickle", "html", "socketserver", "winsound", "_frozen_importlib_external", "warnings", "lzma", "dbm", "threading", "zlib", "smtplib", "marshal", "sysconfig", "contextvars", "difflib", "struct", "colorsys", "genericpath", "lib2to3", "plistlib", "smtpd", "dataclasses", "_sre", "hmac", "signal", "wave", "pyexpat", "base64", "contextlib", "turtle", "poplib", "_tokenize", "xmlrpc", "_bootsubprocess", "faulthandler", "_stat", "_sha512", "numbers", "turtledemo", "copyreg", "array", "_sqlite3", "pydoc", "spwd", "unittest", "idlelib", "abc", "ctypes", "multiprocessing", "tomllib", "_tkinter", "locale", "posixpath", "_codecs_iso2022", "pty", "filecmp", "_thread", "re", "zipapp", "_strptime", "logging", "_collections_abc", "_struct", "keyword", "_winapi", "pipes", "_blake2", "_sha1", "imghdr", "stringprep", "_sitebuiltins", "os", "profile", "types", "typing", "_signal", "sre_parse", "csv", "compileall", "shlex", "nt", "importlib", "symtable", "binascii", "wsgiref", "statistics", "subprocess", "_ast", "ossaudiodev", "_io", "random", "nis", "_codecs_cn", "_uuid", "_decimal", "uuid", "pstats", "_multiprocessing", "curses", "heapq", "_locale", "grp", "_markupbase", "optparse", "_aix_support", "_weakref", "sunau", "math", "ntpath", "tabnanny", "_codecs_tw", "sndhdr", "tkinter", "tokenize", "unicodedata", "ssl", "_collections", "configparser", "zoneinfo", "_symtable", "_multibytecodec", "_posixsubprocess", "bisect", "fnmatch", "_dbm", "audioop", "_queue", "mailcap", "secrets", "runpy", "asyncio", "termios", "shelve", "pyclbr", "venv", "bdb", "_abc", "decimal", "_md5", "queue", "token", "string", "_codecs_kr", "_json", "select", "_csv", "_sha256", "msvcrt", "trace", "pwd", "shutil", "site", "quopri", "_lzma", "zipimport", "cmd", "pdb", "graphlib", "getopt", "platform", "enum", "_codecs", "aifc", "_statistics", "rlcompleter", "xdrlib", "_crypt", "textwrap", "this", "winreg", "_lsprof", "gzip", "linecache", "cgi", "nturl2path", "pydoc_data", "_compat_pickle", "_elementtree", "ensurepip", "gettext", "_operator", "_sha3", "cgitb", "_bisect", "sys", "json", "io", "_msi", "calendar", "operator", "reprlib", "distutils", "imp", "resource", "selectors", "nntplib", "pickletools", "_imp", "_threading_local", "errno", "ipaddress", "glob", "atexit", "telnetlib", "_ssl", "asynchat", "time", "msilib", "_string", "__future__", "concurrent", "opcode", "_contextvars", "pprint", "py_compile", "ftplib", "gc", "bz2", "email", "argparse", "syslog", "tty", "pkgutil", "itertools", "tracemalloc", "inspect", "hashlib", "tarfile", "_heapq", "_socket", "crypt", "ast", "datetime", "_warnings", "_ctypes", "_weakrefset", "_tracemalloc", "_bz2", "modulefinder", "posix", "_overlapped", "_zoneinfo"})

# Save to json
with open("top-pypi-project-names.json", "w") as f:
    json.dump(project_names, f)

print('done')

