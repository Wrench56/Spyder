#!/bin/sh

# Version bump

sed -i "s/VERSION = '.*'/VERSION = '$1'/" src/client/utils/constants.py
