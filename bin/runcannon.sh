#!/bin/bash

pipenv run python mqttinput.py cannon | pipenv run python cannoncontroller.py
