#!/bin/bash
set -eo pipefail

BASE=/home/ghaedi/projects/def-ghaedi/ghaedi/protein/alzheimer/bindcraft

mkdir -p "$BASE/input"
mkdir -p "$BASE/settings"
mkdir -p "$BASE/scripts"
mkdir -p "$BASE/logs"
mkdir -p "$BASE/designs"
mkdir -p "$BASE/designs_p1"
mkdir -p "$BASE/designs_p2"
mkdir -p "$BASE/designs_p3"
mkdir -p "$BASE/designs_p4"
mkdir -p "$BASE/sync/to_frontenac"

echo "Directory structure created under $BASE"
ls -R "$BASE" --ignore=repo
