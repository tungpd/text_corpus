#!/bin/bash
set -e
torify curl http://icanhazip.com/
echo -e 'AUTHENTICATE "123"\r\nsignal NEWNYM\r\nQUIT' | nc 127.0.0.1 9051
torify curl http://icanhazip.com/
