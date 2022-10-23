#!/usr/bin/env python3

import re
import time


def validate_command_is_keyword(cmd):
    return cmd in ["up", "down", "left", "right", "stop", "fire"]


def perform_command(cmd, delay):
    print("Sending command '" + cmd + "'")
    if delay:
        print(f"sleeping {delay}")
        time.sleep(delay / 1000)
        print("Sending 'stop'")
    print("OK")


cmdpattern = re.compile("^([a-z]+)( ([0-9]+))?$")
print(">> Cannon Controller. Use commands up, down, left, right, stop and fire with an optional duration")
while True:
    try:
        cmdline = input()
    except EOFError:
        exit(0)
    if cmdline.strip().startswith("#"):
        print("OK")
    else:
        match = cmdpattern.match(cmdline)
        if match:
            cmd = match.group(1)
            if not validate_command_is_keyword(cmd):
                print("ERROR: Command '" + cmdline + "' is not in up, down, left, right, stop and fire")
            else:
                durationstr = match.group(3)
                if durationstr:
                    if cmd == "fire" or cmd == "stop":
                        print("ERROR: 'fire' and 'stop' does not take arguments")
                    else:
                        duration = int(durationstr)
                        if duration > 10000:
                            print("ERROR: Delay must not be greater than 10000")
                        else:
                            perform_command(cmd, duration)
                    # print("cmd: '" + cmd + "', arg: '" + arg + "'")
                else:
                    perform_command(cmd, None)
        # print("cmd: '" + cmd + "'")
        else:
            print("ERROR: Command '" + cmdline + "' is not in up, down, left, right, stop and fire")
