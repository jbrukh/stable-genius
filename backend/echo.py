import sys
import json

for line in sys.stdin:
    out = {"prompt": line.strip()}
    print(json.dumps(out))