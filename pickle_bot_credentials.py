#!/usr/bin/env python

import pickle

print "This script will pickle a username and password pair as a list."

user = []

user.append(raw_input("Username: "))
user.append(raw_input("Password: "))

filename = raw_input("File name to save to: ")

pickle.dump(user, open(filename, "wb+"))