#!/bin/bash

pipenv run python mqttinput.py thunder | pipenv run python thundercontroller.py
