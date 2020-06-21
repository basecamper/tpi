#!/bin/bash

if [ "$UID" != "0" ]; then
   echo must be root
   exit 1
fi

CONFIG=$(cat config.json)

extract_config_value()
{
   echo "$CONFIG" | grep "$1" | sed -e "s/.*: \"//g" | sed -e "s/[\",]//g"
}

TO_WIPE_CRYPTFILE="to_wipe_cryptfile"
TO_FORMAT_CRYPTFILE="to_format_cryptfile"

CRYPTED_FILE=$( extract_config_value "crypted file" )
PASSWORDS_FILE=$( extract_config_value "passwords file name" )
MOUNT_DIRECTORY=$( extract_config_value "decrypted mount dir" )

DD_COUNT=20
DD_BS="1M"

run_error_cleanup()
{
   [ -d "$MOUNT_DIRECTORY" ] && mountpoint "$MOUNT_DIRECTORY" >/dev/null\
                             && umount "$MOUNT_DIRECTORY"
   [ -e "/dev/mapper/$TO_WIPE_CRYPTFILE" ] && eval "cryptsetup close /dev/mapper/$TO_WIPE_CRYPTFILE"
   [ -e "/dev/mapper/$TO_FORMAT_CRYPTFILE" ] && eval "cryptsetup close /dev/mapper/$TO_FORMAT_CRYPTFILE"
   [ -e "$CRYPTED_FILE" ] && rm "$CRYPTED_FILE"
   [ -d "$MOUNT_DIRECTORY" ] && rmdir "$MOUNT_DIRECTORY"
}

run_cmd()
{
   # $1 cmd
   # $2 set to 0 to disable exiting script
   # $3 set to 1 to show OK no matter what
   eval "$1" >/dev/null 2>&1 && echo "[  OK  ] $1" && return 0
   [ "$3" != "1" ] && echo "[ ERROR ] $1" || echo "[  OK  ] $1"
   [ "$2" == "0" ] && return 1
   run_error_cleanup
   exit 1
}

case "$1" in
   "remove"|"r"|"uninstall"|"u")
      run_error_cleanup
      exit 0
      ;;
esac


if [ ! -d "$MOUNT_DIRECTORY" ]; then
   echo "-- creating mount directory $MOUNT_DIRECTORY --"
   run_cmd "mkdir $MOUNT_DIRECTORY"
   run_cmd "chmod 700 $MOUNT_DIRECTORY"
fi

if [ ! -e "$CRYPTED_FILE" ]; then
   echo "-- creating $CRYPTED_FILE --"
   run_cmd "touch $CRYPTED_FILE"
   run_cmd "chmod 700 $CRYPTED_FILE"
   run_cmd "dd if=/dev/zero of=$CRYPTED_FILE bs=$DD_BS count=$DD_COUNT"
   run_cmd "sync"
   run_cmd "cryptsetup open --type plain -d /dev/urandom $CRYPTED_FILE $TO_WIPE_CRYPTFILE"
   while [ ! -e "/dev/mapper/$TO_WIPE_CRYPTFILE" ]; do
      echo "waiting for cryptdevice /dev/mapper/$TO_WIPE_CRYPTFILE"
      sleep 1
   done
   run_cmd "dd if=/dev/zero of=/dev/mapper/$TO_WIPE_CRYPTFILE bs=$DD_BS count=$DD_COUNT"
   run_cmd "sync"
   run_cmd "cryptsetup close $TO_WIPE_CRYPTFILE"

   run_cmd "cryptsetup -q --use-random --verify-passphrase luksFormat $CRYPTED_FILE"
   run_cmd "cryptsetup open $CRYPTED_FILE $TO_FORMAT_CRYPTFILE"
   run_cmd "dd if=/dev/zero of=/dev/mapper/$TO_FORMAT_CRYPTFILE status=progress" 0 1
   run_cmd "sync"
   run_cmd "mkfs.ext4 /dev/mapper/$TO_FORMAT_CRYPTFILE"
   run_cmd "sync"
   run_cmd "mount /dev/mapper/$TO_FORMAT_CRYPTFILE $MOUNT_DIRECTORY"
   run_cmd "touch $MOUNT_DIRECTORY/$PASSWORDS_FILE"
   run_cmd "umount $MOUNT_DIRECTORY"
   run_cmd "cryptsetup close $TO_FORMAT_CRYPTFILE"
fi