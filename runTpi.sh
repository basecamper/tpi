#!/bin/bash

if [ "$UID" != "0" ]; then
	echo "must be root"
	exit 1
fi

COMMAND="python3 ./tpi.py"

case "$1" in
	"-d"|"d"|"debug")
		eval  "$COMMAND debug"
		;;
	*)
		eval  "$COMMAND" >/dev/tty1 >&1
		;;
esac

