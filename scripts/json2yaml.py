#!/usr/bin/env python3

import json
import yaml
import sys



if __name__ == '__main__':

    data = json.load(sys.stdin)
    yaml.dump(data, sys.stdout)
