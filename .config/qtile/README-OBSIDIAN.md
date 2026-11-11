# Qtile Obsidian

Rediseño gráfico de Qtile para Arch Linux sobre **X11**.

## Cambios

- Barra superior de 38 px con margen y borde discreto.
- Tema grafito, tipografía JetBrainsMono Nerd Font, acento verde azulado.
- Grupos 01–08 (Super+1...8), sin iconos inconsistentes.
- CPU, RAM, tráfico agregado de red (Ethernet y VPN), actualizaciones Arch y reloj.
- MonadTall inicial, gaps de 10 px y foco con borde de 2 px.
- Systray solo en pantalla principal; autostart para Picom, Dunst, nm-applet y udiskie.
- Actualización de imports lazy en los atajos y ratón sin cambiar sus acciones.

## Dependencias

    sudo pacman -S --needed qtile python-psutil ttf-jetbrains-mono-nerd rofi pacman-contrib picom dunst network-manager-applet udiskie feh

## Despliegue

    cp -a ~/.config/qtile ~/.config/qtile.backup.$(date +%Y%m%d-%H%M%S)
    python -m compileall -q ~/.config/qtile
    qtile check

Si la validación pasa, recarga Qtile con Super+Ctrl+R.
Reinicia sesión para ejecutar startup_once.

## Alcance

- Tema: themes/obsidian.json (focus, color3).
- Fondo: ~/Images/wallpaper/wallpaper-4.jpg.
- Soporte: Qtile sobre X11 (usa xrandr, Picom, Feh y Systray).
- No validado visualmente en una sesión Qtile/NVIDIA real.
