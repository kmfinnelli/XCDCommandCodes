#! /bin/bash
#stty -F /dev/ttyUSB0 115200
echo -e '\xE4\xA5\x00\xD5\x0F\x03\x01\x0E\x09\x06\x06\xE8\x03\x01\x00\x00\x00\0xDA' > /dev/ttyUSB0
