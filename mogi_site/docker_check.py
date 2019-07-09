import os
import re
def is_docker():
    # https://stackoverflow.com/questions/43878953/how-does-one-detect-if-one-is-running-within-a-docker-container-within-python
    path = "/proc/" + str(os.getpid()) + "/cgroup"
    if not os.path.isfile(path):
        return False

    with open(path) as f:
        for line in f:
            if re.match("\d+:[\w=]+:/docker(-[ce]e)?/\w+", line):
                return True
        return False