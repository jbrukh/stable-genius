import sys
import json

for line in sys.stdin:
    out = {"prompt": line}
    print(json.dumps(out))