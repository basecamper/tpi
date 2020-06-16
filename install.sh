#!/bin/bash

if [ "$UID" != "0" ]; then
	echo must be root
	exit 1
fi

# nothing yet - create config json here as well