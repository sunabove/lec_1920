alias a='alias'
alias c='clear'
alias vb='vi ~/.bashrc'
alias sb='source ~/.bashrc'
alias xt="xterm -fa 'Monospace' -fs 14 &" 
alias video="raspivid -n -t 0 -h 720 -w 1080 -fps 15 -b 2000000 -l -o tcp://0.0.0.0:3333"
alias gps_log="sudo cat /dev/serial0 | tee ~/`date +'%Y%m%d-%H-%M-%S'`.nmea"

alias cam="raspivid -t 999999 -fps 25 -b 2000000 -vf -hf -n -o - | tee video_`date '+%Y-%m-%d_%H:%M:%S'`.h264 | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay ! udpsink   host=`who --ips | awk '{print $5}'` port=5600"

#raspivid -t 999999 -h 720 -w 1080 -fps 25 -hf -b 2000000 -o - | tee YOURFILENAME.h264 | gst-launch-1.0 -v fdsrc ! h264parse !  rtph264pay config-interval=1 pt=96 ! gdppay ! tcpserversink host=YOUR-PI-IP-ADDRESS port=5000 

#cd ~/ads
#clear

