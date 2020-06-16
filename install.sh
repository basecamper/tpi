#!/bin/bash

CONFIG=$(cat config.json)

extract_config_value()
{
   echo "$CONFIG" | grep "$1" | sed -e "s/.*: \"//g" | sed -e "s/\",//g"
}

CRYPTED_FILE=$( extract_config_value "crypted file" )
MOUNT_DIRECTORY=$( extract_config_value "decrypted mount dir" )

if [ "$UID" != "0" ]; then
   echo must be root
   exit 1
fi

run_cmd()
{
   eval "$1" && echo "[  OK  ] $1" && return 0
   echo "[ ERROR ] $1" && exit 1
}

[ ! -e "$CRYPTED_FILE" ] && run_cmd "touch $CRYPTED_FILE"\
                         && run_cmd "dd if=/dev/zero of=$CRYPTED_FILE bs=1M count=2"

[ ! -d "$MOUNT_DIRECTORY" ] && run_cmd "mkdir $MOUNT_DIRECTORY"\
                            && run_cmd "chmod 700 $MOUNT_DIRECTORY"