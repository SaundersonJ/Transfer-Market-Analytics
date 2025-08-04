#!/bin/bash

cat | xargs -I CMD -P 16 bash -c CMD

