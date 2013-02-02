
import sys
import serial
from os import system
from keys import KEYS

MAX_DIFF = 500
SAVE_NEW_SIGNALS = False

try:
    s = serial.Serial("/dev/ttyACM0", 9600)
except:
    s = serial.Serial("/dev/ttyACM1", 9600)

s.setTimeout(0.01)

def find_key(nums):
    diff = 0
    print
    print "Length: ", len(nums)
    for key in KEYS:
        for i in range(len(KEYS[key])):
            try:
                diff = diff + ((KEYS[key][i] - int(nums[i])) ** 2)
            except Exception,e:
                print e
                break
        diff = diff / 1000
        print key, diff 
        if diff < MAX_DIFF:
            print "RUNNING KEY ", key
            system("xdotool key " + key)
            return


def decode(c):
    lines = c.split("\n")
    nums = []
    for line in  lines[2:-2]:
        on, off = line.split(",")
        on = on.strip()
        off = off.strip()
        nums = nums + [on, off]

    # Ignore short signals
    if len(nums) < 10: 
        print "Code length: ", len(nums), "too short"
        return

    find_key(nums)
    if SAVE_NEW_SIGNALS:
        if "y" == raw_input("Save this signal?"):
            print_signal(nums, "keys.py")

def print_signal(nums, path = None):
    if path != None:
        f = open(path, "ab")
    else:
        f = sys.stdout
    f.write("\n[" + str(nums[0]))

    for num in nums[1:]:
        f.write(", " + str(num))
    f.write("]")
    if path != None:
        f.close()

while True:
    c = s.read(2000)
    if c != "":
        decode(c)


