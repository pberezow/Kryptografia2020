#!/bin/bash

# Small utility for creating keystores
# ./gen_key.sh KEYSTORE PASSWORD IDENT

if [[ $# -lt 3 ]]; then
    echo "Not enough arguments"
    echo "Usage $0 KEYSTORE PASSWORD IDENT"
    exit
fi

keytool -genseckey \
    -keyalg AES -keysize 128 \
    -keystore $1  -storetype jceks\
    -storepass $2 \
    -alias $3 -keypass $2 \
