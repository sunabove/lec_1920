alias c='clear'
alias vb='vi ~/.bashrc'
alias sb='source ~/.bashrc'
alias xt="xterm -fa 'Monospace' -fs 14 &" 
alias python="python3"
alias video="raspivid -n -t 0 -h 720 -w 1080 -fps 15 -b 2000000 -l -o tcp://0.0.0.0:3333"
alias gps_log="sudo cat /dev/serial0 | tee ~/`date +'%Y%m%d-%H-%M-%S'`.nmea"

cd !~ads/gps
clear

