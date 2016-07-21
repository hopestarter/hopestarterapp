#!/bin/sh

if [ -z "$VAULT_LPASS_UID" ] ; then
    echo "No vault UID in environment. Export 'VAULT_LPASS_UID' please."
    exit 1
fi
lpass show --color=never $VAULT_LPASS_UID|tail -n 1 |sed -e 's/.*[ ]//'
