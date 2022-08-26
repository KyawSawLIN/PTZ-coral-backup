# this code is for controlling PTS-303Z in exact angle control
# pan position ranges from 0-350
# tilt position ranges from 0-60
# type Ctrl+C (keyboard interrupt) for breaking while loop s

import serial
import time

ser = serial.Serial("/dev/ttymxc2", 2400)  # 2400 baud rate


def toHex(dec):  # convert dec to hex without '0x' included
    digits = "0123456789ABCDEF"
    x = (dec % 16)
    rest = dec // 16
    if (rest == 0):
        return digits[x]
    return toHex(rest) + digits[x]


def checksum(str):  # checksum calculator
    c = 0
    str = bytes.fromhex(str)
    for i in range(5):
        c = c + str[i]  # combining total values of each byte
    c = c % 256  # take modulo 256
    #print('checksum value = ', toHex(c))
    return toHex(c)


def read_position():

    ser.write(bytes.fromhex('FF 07 00 51 00 00 58'))
    #time.sleep(0.1)
    pan_read = ser.read(7)

    ser.write(bytes.fromhex('FF 07 00 53 00 00 5A'))
    #time.sleep(0.1)
    tilt_read = ser.read(7)

    return pan_read, tilt_read


def print_position(a):

    q1 = toHex(a[4])
    q2 = toHex(a[5])

    q_3 = '{0:0>2s}{1:0>2s}'.format(q1, q2)
    q_final = round((int(q_3, 16) / 100))
    return q_final


def mod(num):  # this function is for converting angle values to real values used in pelco command
    d = num*100
    return d


def pan(var):  # for generating pan command in pelco-d

    # this is incomplete output string.var is modulated angle user input(MAUI). this line is to format MAUI with required pelco commands in string format
    txp1 = '07 00 4B {0:0>4s}'.format(var)

    checksum_result = checksum(txp1)

    # add checksum to output string
    txp2 = 'FF {0} {1:0>2s}'.format(txp1, checksum_result)
    print('output         = ', txp2)  # for debugging
    print()  # for asthetics

    ser.write(bytes.fromhex(txp2))  # serially transmit data over pyserial


def tilt(var):

    txt1 = '07 00 4D {0:0>4s}'.format(var)

    checksum_result = checksum(txt1)

    txt2 = 'FF {0} {1:0>2s}'.format(txt1, checksum_result)
    print('output         = ', txt2)
    print()

    ser.write(bytes.fromhex(txt2))


while True:

    reading = read_position()
    print('current position ...\t pan: {0} ||  tilt: {1}'.format(
        print_position(reading[0]), print_position(reading[1])))

    z = input("Type (p) for pan and (t) for tilt : ")

    if z == 'p':
        f = int(input('Type pan degree 0 to 350: '))

        if f != int(print_position(reading[0])):

            tmp = mod(f)
            var_0 = toHex(tmp)
            pan(var_0)
        else:
            print("You enter current pan position \n")

    elif z == 't':
        f = int(input('type pan degree 0 to 60: '))

        if f != int(print_position(reading[1])):

            tmp = mod(f)
            var_0 = toHex(tmp)
            tilt(var_0)

        else:
            print("You enter current tilt position \n")

    else:
        continue