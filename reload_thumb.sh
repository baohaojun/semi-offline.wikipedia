#!/bin/bash

eval $(for x in `ls -l /proc/$$/fd |grep -P 'socket:\[\d+\]'|pn 9`; do echo exec $x\>/dev/null\;; done)
    (
        ((x=0))
        while ps -eo cmd|grep -v 'grep -q -e' 2>/dev/null|grep -q -e 'bash.*wiki-cache.*job'; do 
            echo still have `ps -eo cmd|grep -e 'bash.*job'|wc -l` wiki thumb cache thread running
            sleep 5
            if (( x++ >= 60)); then
                echo waited for 5 minutes, exiting...
                exit
            fi
        done

        "$@" 

        ((x=0))
        while ps -eo cmd|grep -v 'grep -q -e' 2>/dev/null|grep -q -e 'bash.*wiki-cache.*job'; do 
            echo after load thumb, still have `ps -eo cmd|grep -e 'bash.*job'|wc -l` wiki thumb cache thread running
            sleep 5
            if (( x++ >= 60)); then
                echo waited for 5 minutes, exiting...
                exit
            fi
        done
	notify-send -t 2000 'Your wikimedia thumb cache is complete'
	aplay /usr/share/sounds/purple/login.wav

    )&
