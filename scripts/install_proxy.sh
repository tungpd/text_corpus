#!/bin/bash
set -e
SCRIPTS_DIR="`pwd`"
ROOT_DIR="$SCRIPTS_DIR/.."
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
cd $ROOT_DIR/third_parties/polipo
make all
make install
echo "socksParentProxy = 127.0.0.1:9050" >> /etc/polipo/config
echo 'diskCacheRoot=""' >> /etc/polipo/config
echo 'disableLocalInterface=true' >> /etc/polipo/config
cp $SCRIPTS_DIR/polipo.service /etc/systemd/system/
systemctl start polipo
systemctl status polipo


