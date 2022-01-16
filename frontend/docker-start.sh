#!/bin/sh
cp -vr static/* static_files/
yarn build && yarn start