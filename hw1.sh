#!/bin/sh
set -e -o pipefail
git clone git@github.com:linnil1/2021summer_lesson1.git
cd 2021summer_lesson1
git branch add_linnil1_hw1
git checkout add_linnil1_hw1
mkdir -p HW1/Answer
echo -e $(find HW1 -name findme.tar.gz) > HW1/Answer/linnil1.txt
git add HW1/Answer/linnil1.txt
git commit -m "Add linnil1 HW1"
git push --set-upstream origin add_linnil1_hw1
