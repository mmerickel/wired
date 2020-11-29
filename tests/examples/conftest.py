import sys

if sys.version_info < (3, 7):  # pragma: no cover
    collect_ignore_glob = ['*.py']
else:
    pass
