#!/bin/bash

# Usage: (from this directory)
# - `../run.py java.sh --log --students 40 --groups 6` etc

javac Solution.java
java Solution $1 $2
