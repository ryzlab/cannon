#!/usr/bin/env python3

import re
import time
import hid

commands = {
    'up': 0x01,
    'down': 0x02,
    'left': 0x04,
    'right': 0x08,
    'fire': 0x10,
    'stop': 0x20
}


def validate_command_is_keyword(cmd):
    return cmd in ["up", "down", "left", "right", "stop", "fire"]


def perform_command(hidraw, cmd, delay):
    print("Sending command '" + cmd + "'")
    hidraw.write([commands[cmd]])
    if delay:
        print(f"sleeping {delay}")
        time.sleep(delay / 1000)
        print("Sending 'stop'")
        hidraw.write([commands['stop']])
    print("OK")

hidraw = hid.device(0x1941, 0x8021)
hidraw.open(0x1941, 0x8021)


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
                            perform_command(hidraw, cmd, duration)
                    # print("cmd: '" + cmd + "', arg: '" + arg + "'")
                else:
                    perform_command(hidraw, cmd, None)
        # print("cmd: '" + cmd + "'")
        else:
            print("ERROR: Command '" + cmdline + "' is not in up, down, left, right, stop and fire")
