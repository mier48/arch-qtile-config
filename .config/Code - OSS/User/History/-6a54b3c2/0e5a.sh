#!/bin/sh

# Volume
volumeicon &
# Network
nm-applet &
# Bluetooth
blueman-applet &
# Usb disks
udiskie -t &
# Battery
cbatticon &
# Wallpaper
feh --bg-scale Images/wallpaper/wallpaper-1.jpg
# Double Screen
#xrandr --output eDP --primary --mode 1920x1080 --pos 0x0 --rotate normal --output HDMI-A-0 --mode 1920x1080 --pos 1920x0 --rotate normal
# Themes
picom &
