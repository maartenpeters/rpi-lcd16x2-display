#!/usr/bin/python
import time
import re
from subprocess import *
from lcd import *

def run_cmd(cmd):
    try:
        p = Popen(cmd, shell=True, stdout=PIPE, encoding="ascii")
        output = p.communicate()[0]
    except Exception as e:
        output = ""
    return output


def show_msg(msg, slp=3.0):
    lcd.clear()
    lcd.message = msg
    time.sleep(slp)


while True:
    # Internal IP address
    inet = run_cmd("hostname -I | cut -d ' ' -f 1")
    # External IP address
    exnet= run_cmd("wget http://ipinfo.io/ip -qO -")
    # Raspberry Pi CPU temperature
    tempcpu = run_cmd("cat /sys/class/thermal/thermal_zone0/temp | awk 'NR == 1 { print $1 / 1000}' | cut -c -4")
    # Raspberry Pi GPU temperature
    tempgpu = run_cmd("/opt/vc/bin/vcgencmd measure_temp | cut -c 6- | cut -c -4")
    # CPU usage
    usagecpu = run_cmd("bash cpu_usage.sh | cut -c -4")
    # Memory usage 
    usagemem = run_cmd("free | awk 'FNR == 3 {print $3/($3+$4)*100}' | cut -c -4")
    # Get free disk space
    freedisk = run_cmd("df -h | sed -n 2p | awk '{ printf $4 }'")
    # Get used disk space
    useddisk = run_cmd("df -h | sed -n 2p | awk '{ printf $3 }'")
    # Calculate RX rate
    rx = run_cmd("bash rx.sh")
    # Calculate TX rate
    tx = run_cmd("bash tx.sh")

    # Print internal and external IP address
    show_msg(f"{str(inet)}\n{str(exnet)}")
    
    # Print Raspberry Pi CPU and GPU temperature
    # degree symbol
    lcd.create_char(1, [6,9,9,6,0,0,0])
    show_msg(f"CPU: {str(tempcpu)}\x01C\nGPU: {str(tempgpu)}\x01C")

    # Print CPU and Memory Usage
    show_msg(f"CPU: {str(usagecpu)}%\nMem.: {float(usagemem):.2%}")
    
    # Print disk space
    clean = lambda x: x.replace("\n","").strip()
    freedisk = re.findall("[0-9A-z\.]+", freedisk)[0]
    useddisk = re.findall("[0-9A-z\.]+", useddisk)[0]
    show_msg(f"Free: {str(freedisk)}\nUsed: \n{str(useddisk)}")

    # Print network speed
    show_msg(f"Rx KB/s: {str(rx)}\nTx KB/s: {str(tx)}")