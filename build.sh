#!/bin/bash

rm dist/*

python3 setup.py sdist bdist_wheel

if [ "$1" = "--deploy" ];
then
    twine upload dist/*
    echo 'Deploy DONE'
fi