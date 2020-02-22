#!/bin/bash
set -e
apt update
apt install -y tor
apt install -y netcat
echo "ControlPort 9051" >> /etc/tor/torrc
echo HashedControlPassword $(tor --hash-password "tor" | tail -n 1) >> /etc/tor/torrc
tail -n 2 /etc/tor/torrc
service tor restart
service tor status
echo -e 'AUTHENTICATE "tor"' | nc 127.0.0.1 9051
apt install -y curl
curl http://ipv4.icanhazip.com/
torify curl http://ipv4.icanhazip.com/
cp ./change_ip.sh /usr/local/bin/
crontab -l > /tmp/mycron
echo '0 0 * * * /usr/local/bin/change_ip.sh' >> /tmp/mycron
crontab /tmp/mycron

