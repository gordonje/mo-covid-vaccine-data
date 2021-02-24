#!/bin/bash
# prepare a source code package

# pip install --upgrade --target package/ -r requirements.txt
# cd package
# zip -r9 ${OLDPWD}/package.zip .
# cd ${OLDPWD}

zip -g -r package.zip function.py
zip -g -r package.zip s3.py

# rm -rf package