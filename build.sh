#!/bin/bash

cd static
yarn
elm make src/HomePage.elm --output elm.js
