#!/bin/bash
SWITCH_PIN="13 24 12 16 21"
while true; do
    for PIN in $SWITCH_PIN
    do
        PIN_STATE=`gpio -g read $PIN`
        if [ $PIN_STATE = 1 ]; then
            if [ $PIN = 13 ]; then
                echo "a"
            elif [ $PIN = 24 ]; then
                echo "i"
            elif [ $PIN = 12 ]; then
                echo "u"
            elif [ $PIN = 16 ]; then
                echo "e"
            elif [ $PIN = 21 ]; then
                echo "o"
            fi
            sleep 0.3
        fi
    done
done
