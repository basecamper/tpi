#!/bin/bash

if [ "$UID" != "0" ]; then
   echo must be root
   exit 1
fi

CONFIG=$(cat config.json)
extract_config_value()
{
   echo "$CONFIG" | grep "$1" | sed -e "s/.*: \"//g" | sed -e "s/\",//g"
}
run_cmd()
{
   # $1 cmd
   # $2 set to 0 to disable exiting script
   # $3 set to to show OK no matter what
   eval "$1" && echo "[  OK  ] $1" && return 0
   [ "$3" != "1" ] && echo "[ ERROR ] $1" || echo "[  OK  ] $1"
   [ "$2" == "0" ] && return 1
   exit 1
}

CRYPTED_FILE=$( extract_config_value "crypted file" )
MOUNT_DIRECTORY=$( extract_config_value "decrypted mount dir" )

DD_COUNT=2
DD_BS="1M"

if [ ! -e "$CRYPTED_FILE" ]; then
   run_cmd "touch $CRYPTED_FILE"\
      && run_cmd "chmod 700 $CRYPTED_FILE"\
      && run_cmd "dd if=/dev/zero of=$CRYPTED_FILE bs=$DD_BS count=$DD_COUNT"

   if run_cmd "cryptsetup open --type plain -d /dev/urandom $CRYPTED_FILE to_wipe"; then
      while [ ! -e "/dev/mapper/to_wipe" ]; do
         echo "waiting for cryptdevice to wipe"
         sleep 1
      done
      run_cmd "dd if=/dev/zero of=/dev/mapper/to_wipe bs=$DD_BS count=$DD_COUNT status=progress"
      run_cmd "cryptsetup close /dev/mapper/to_wipe"
   fi
fi

[ ! -d "$MOUNT_DIRECTORY" ] && run_cmd "mkdir $MOUNT_DIRECTORY"\
                            && run_cmd "chmod 700 $MOUNT_DIRECTORY"