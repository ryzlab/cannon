#!/usr/bin/env python3

import re
import hid
import threading as th


class CannonController:
    class Command:
        def __init__(self, command_name, hid_code, takes_argument):
            self.command_name = command_name
            self.hid_code = hid_code
            self.takes_argument = takes_argument

    UP = Command("up", 0x01, True)
    DOWN = Command("down", 0x02, True)
    LEFT = Command("left", 0x04, True)
    RIGHT = Command("right", 0x08, True)
    FIRE = Command("fire", 0x10, True)
    STOP = Command("stop", 0x20, False)

    __commands = {UP, DOWN, LEFT, RIGHT, FIRE, STOP}

    def __init__(self):
        try:
            self.hidraw = hid.device(0x1941, 0x8021)
            self.hidraw.open(0x1941, 0x8021)
        except OSError:
            print("No cannon found. Continuing without hardware")
            self.hidraw = None
        self.thread = None

    @classmethod
    def valid_command_name(cls, command_name):
        for command in cls.__commands:
            if command.command_name == command_name:
                return True
        return False

    @classmethod
    def name_to_command(cls, command_name):
        for command in cls.__commands:
            if command.command_name == command_name:
                return command
        raise ValueError("Unknown command name " + command_name)

    def __stop_callback(self):
        # print("STOPPING")
        if self.hidraw is not None:
            self.hidraw.write([CannonController.STOP.hid_code])

    def send_command(self, command, delay=None):
        # print("Sending command '" + cmd + "'")
        if self.thread is not None:
            self.thread.cancel()
            self.thread = None
        if self.hidraw is not None:
            self.hidraw.write([command.hid_code])
        if delay:
            self.thread = th.Timer(delay / 1000, self.__stop_callback)
            self.thread.start()


cannon_controller = CannonController()
command_pattern = re.compile("^([a-z]+)( ([0-9]{1,5}))?$")

print(">> Cannon Controller. Use commands up, down, left, right, stop and fire with an optional duration")
while True:
    try:
        input_line = input().strip()
    except EOFError:
        exit(0)
    if input_line.startswith("#"):
        print("OK")
        continue

    match = command_pattern.match(input_line)

    if not match:
        print("ERROR: Input '" + input_line + "' is invalid")
        continue

    cmd = match.group(1)
    if not CannonController.valid_command_name(cmd):
        print("ERROR: Command '" + input_line + "' is unknown")
        continue

    cannon_command = CannonController.name_to_command(cmd)
    duration_str = match.group(3)
    if not duration_str:
        cannon_controller.send_command(cannon_command, None)
        print("OK: " + input_line)
        continue

    if not cannon_command.takes_argument:
        print("ERROR: Command '" + cannon_command.command_name + "' does not take arguments")
        continue

    duration = int(duration_str)
    if duration > 10000:
        print("ERROR: Delay must not be greater than 10000")
        continue

    cannon_controller.send_command(cannon_command, duration)
    print("OK: " + input_line)
