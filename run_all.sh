#!/bin/bash

cd scrapers
sh "scrape_all.sh"
cd ..

python "analyze.py"
python "summarize.py"
cd summaries
python "summary.py"