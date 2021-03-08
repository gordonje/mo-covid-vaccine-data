#!/bin/bash
# prepare a source code package

# add dependencies
pip install --upgrade --target package/ -r requirements.txt
cd package
zip -r9 ${OLDPWD}/package.zip .
rm -rf package
cd ${OLDPWD}

# add source code
zip -g -r package.zip templates/*
zip -g -r package.zip function.py
zip -g -r package.zip s3.py
