#!/bin/bash
set -evx

mkdir ~/.historiacore

# safety check
if [ ! -f ~/.historiacore/.historia.conf ]; then
  cp share/historia.conf.example ~/.historiacore/historia.conf
fi
