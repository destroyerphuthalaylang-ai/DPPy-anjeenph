#!/usr/bin/env python3
import sys

if len(sys.argv) > 1:
    print("none")
else:
    i = 0
    while i <= 10:
        table = "Table de " + str(i) + ":"
        j = 0
        while j <= 10:
            table = table + " " + str(i * j)
            j = j + 1
        print(table)
        i = i + 1
