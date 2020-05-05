alias a='alias'
alias c='clear'
alias vb='vi ~/.bashrc'
alias sb='source ~/.bashrc'
alias xt="xterm -fa 'Monospace' -fs 14 &" 
alias python="python3"
alias video="raspivid -n -t 0 -h 720 -w 1080 -fps 15 -b 2000000 -l -o tcp://0.0.0.0:3333"
alias gps_log="sudo cat /dev/serial0 | tee ~/`date +'%Y%m%d-%H-%M-%S'`.nmea"

alias cam="raspivid -t 0 -fps 24 -b 2000000 -vf -hf -n -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay ! udpsink  host=`who --ips | awk '{print $5}'` port=5600"

#cd ~/ads
#clear

