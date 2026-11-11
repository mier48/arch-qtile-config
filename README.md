# Arch Linux · Qtile Obsidian

Configuración de **Arch Linux + Qtile (X11) + Alacritty + Fish + Fastfetch + Rofi + Dunst + Picom**, diseñada para productividad con teclado y monitor ultrawide. Un solo lenguaje visual: fondo grafito, texto claro y acento verde azulado.

> Repositorio de dotfiles, no instalador de Arch Linux. No configura drivers NVIDIA, cifrado, display manager, red ni hardening. **Solo Qtile sobre X11**: utiliza xrandr, picom, feh y Systray, no Qtile Wayland.

## Estructura

| Ruta | Función |
| --- | --- |
| .config/qtile/config.py | Configuración principal y hook startup_once |
| .config/qtile/settings/ | Atajos, grupos, layouts, widgets, pantallas, ratón y tema |
| .config/qtile/themes/obsidian.json | Paleta de Qtile |
| .config/qtile/autostart.sh | Inicio de servicios, red, USB y fondo |
| .config/alacritty/alacritty.toml | Terminal TOML y shell Fish |
| .config/alacritty/themes/obsidian.toml | Paleta ANSI |
| .config/fish/ | Prompt nativo, Git, colores y abreviaturas |
| .config/fastfetch/config.jsonc | Información del equipo con módulos y paleta Obsidian |
| .config/rofi/ | Lanzador, cambio de ventanas y menú de energía |
| .config/dunst/dunstrc | Notificaciones Obsidian |
| .config/picom/picom.conf | Composición GLX, sombras y esquinas |
| .config/qtile/scripts/power-menu.sh | Menú de sesión/energía con confirmaciones |
| .config/qtile/wallpapers/obsidian.svg | Fondo vectorial editable, 3440 × 1440 |
| .bashrc | Fallback Bash opcional |

Las carpetas GTK, estados de Fish, cachés Python y temas históricos no forman parte de esta configuración distribuible.

## Diseño

| Elemento | Color |
| --- | --- |
| Fondo | #111820 |
| Superficie | #18232E |
| Borde | #35434F |
| Texto | #C9D6E1 |
| Destacado | #EDF3F8 |
| Acento/foco | #82CDBE |
| Alerta | #E78991 |

Qtile: barra de **38 px**, grupos **01–08**, CPU, RAM, tráfico de red y reloj; layouts MonadTall (principal), Bsp, MonadWide y Max, con márgenes de 10 px y foco de 2 px. El widget Net suma las interfaces activas; sin Wi-Fi fijada ni batería.

Alacritty: JetBrainsMono Nerd Font a 12,5 puntos, 0,97 de opacidad, TOML y Fish. Fish: prompt nativo de dos líneas, Git, Python venv, códigos de error, duración y hora. Fastfetch se ejecuta con `sys` y, opcionalmente, al iniciar Fish. No se ejecuta automáticamente por defecto. Los colores están coordinados, pero **deben sincronizarse manualmente** si cambias la paleta.

## Dependencias

Instala Arch Linux + Xorg + Qtile X11 y los paquetes directamente utilizados:

~~~bash
sudo pacman -S --needed \
  git qtile python-psutil alacritty fish fastfetch \
  ttf-jetbrains-mono-nerd xorg-xrandr xorg-xsetroot \
  rofi picom dunst papirus-icon-theme librsvg \ 
  i3lock xss-lock network-manager-applet udiskie \
  feh scrot thunar pacman-contrib
~~~

Opcionales:

~~~bash
sudo pacman -S --needed eza zoxide brightnessctl
~~~

El applet de red requiere NetworkManager funcionando. El volumen usa pactl y requiere PulseAudio o PipeWire-Pulse. brightnessctl solo funciona en hardware compatible. Los atajos de aplicaciones externas requieren instalar esas aplicaciones.

## Instalación segura

~~~bash
git clone https://github.com/mier48/arch-qtile-config.git
cd arch-qtile-config
mkdir -p "$HOME/.config"
stamp=$(date +%Y%m%d-%H%M%S)
for component in qtile fish alacritty fastfetch rofi dunst picom; do
  if [ -e "$HOME/.config/$component" ]; then
    mv "$HOME/.config/$component" "$HOME/.config/$component.backup.$stamp"
  fi
  cp -a ".config/$component" "$HOME/.config/$component"
done
~~~

Este procedimiento sustituye **solo esos siete directorios** y mantiene los anteriores como respaldo. No copies todo .config ni sobrescribas .bashrc automáticamente. No se incluyen archivos Fish generados (fish_variables), MIME ni ajustes GTK. Alacritty arranca Fish sin cambiar el login shell global.

### Sesión Qtile

- Con SDDM, LightDM u otro display manager, selecciona **Qtile (X11)**. El hook startup_once inicia los servicios desde autostart.sh sin .xprofile.
- Con startx, instala xorg-xinit y añade al final de ~/.xinitrc:

~~~sh
exec qtile start
~~~

El fondo original está en `.config/qtile/wallpapers/obsidian.svg`. Durante el arranque, `rsvg-convert` lo convierte a 3440 × 1440 y lo guarda en caché (`~/.cache/obsidian/`); `feh` lo adapta a la pantalla. Si falla la conversión, se muestra un fondo sólido #111820. Puedes sustituir el SVG sin alterar la configuración de Qtile.

## Atajos principales

Super es la tecla Windows/Super.

| Atajo | Acción |
| --- | --- |
| Super + Enter | Alacritty + Fish |
| Super + 1…8 | Cambiar grupo |
| Super + Shift + 1…8 | Mover ventana al grupo |
| Super + h/j/k/l | Izquierda/abajo/arriba/derecha |
| Super + Shift + h/j/k/l | Reordenar ventanas |
| Super + Ctrl + h/j/k/l | Redimensionar en layouts compatibles |
| Super + Tab | Siguiente layout |
| Super + w | Cerrar ventana |
| Super + e | Thunar |
| Super + m | Rofi aplicaciones |
| Super + Shift + m | Rofi ventanas |
| Super + Shift + p | Menú Obsidian de energía |
| Super + Shift + n | Recuperar notificación anterior (Dunst) |
| Super + s / Super + Shift + s | Captura completa / selección |
| Super + Ctrl + r | Recargar Qtile |
| Super + Ctrl + q | Salir de Qtile |

Super + r abre el comando integrado de Qtile. Los demás atajos de apps están en .config/qtile/settings/keys.py.

## Escritorio Obsidian · fase 1

- **Rofi** (`.config/rofi/`): lanzador de aplicaciones (`Super+m`), selector de ventanas (`Super+Shift+m`) y tema Rasi de 720 px con búsqueda central, iconos Papirus-Dark y selección discreta.
- **Dunst** (`.config/dunst/dunstrc`): notificaciones en la pantalla enfocada, esquinas redondeadas, separación de 9 px, barra de progreso y urgencias codificadas con el color de alerta.
- **Picom** (`.config/picom/picom.conf`): backend GLX, VSync, sombras suaves y esquinas de 9 px, sin blur ni transparencias forzadas. La composición depende del driver y puede requerir ajustes en NVIDIA.
- **Fondo Obsidian** (`.config/qtile/wallpapers/obsidian.svg`): vector editable y reproducible; `rsvg-convert` genera una imagen de 3440 × 1440 una sola vez o cuando cambia el SVG. Sin descargas ni dependencias externas durante el arranque.
- **Menú de energía** (`Super+Shift+p`): bloquear, suspender, cerrar sesión, reiniciar o apagar. Exige confirmación para acciones disruptivas y **no ejecuta entradas arbitrarias**. El bloqueo de sesión usa i3lock; xss-lock garantiza que se invoque al suspender mediante logind.
- **Barra Qtile**: botón de energía al extremo derecho que abre el mismo menú.

Para probar Dunst: `dunstify "Obsidian" "Notificación de prueba"`. Para probar Rofi: `rofi -show drun`. Para probar Picom: `picom --config ~/.config/picom/picom.conf` (si ya hay otro compositor activo, no ejecutes una segunda instancia).

**Seguridad del bloqueo:** el menú suspende únicamente si detecta xss-lock e i3lock activos. Antes de depender de esta opción, comprueba desde una sesión real que i3lock bloquea y que al reanudar exige autenticación. Este bloqueo es funcional, pero no constituye todavía un tema personalizado de pantalla de bloqueo (fase 2). Los mecanismos de suspensión de otras aplicaciones o de la BIOS no quedan cubiertos por este menú.

## Fastfetch · Obsidian

La configuración reside en **.config/fastfetch/config.jsonc**, se detecta automáticamente al ejecutar `fastfetch` y está integrada con la abreviatura **`sys`** de Fish. Utiliza el logo pequeño de Arch en verde azulado y tres bloques: **Sistema** (SO, kernel, actividad, paquetes), **Entorno** (Qtile, terminal, shell y pantalla) y **Hardware** (modelo, CPU, GPU, memoria y disco raíz). La fila final muestra la paleta ANSI del terminal Alacritty.

- Ejecución puntual: `fastfetch` o `sys` dentro de Fish.
- Activar al abrir una nueva terminal interactiva: `set -U OBSIDIAN_FASTFETCH_AUTOSTART 1`.
- Desactivar: `set -U OBSIDIAN_FASTFETCH_AUTOSTART 0`.
- El inicio automático **está desactivado por defecto**, se omite por SSH y no se repite en shells Fish anidados.
- No consulta IP pública, tiempo meteorológico ni servicios externos; tampoco utiliza módulos `Command` ni ejecuta procesos arbitrarios. Los valores de hardware se detectan dinámicamente, sin fijar un modelo de CPU o GPU.
- No almacenes detalles privados del equipo en capturas públicas sin revisarlas.

Para modificar los colores, mantén consistentes los hexadecimales de **.config/fastfetch/config.jsonc** con los temas de Qtile, Alacritty y Fish. Fastfetch utiliza el formato JSONC oficial; el archivo distribuido es JSON estricto válido para facilitar su validación.

## Comprobaciones

~~~bash
python -m compileall -q "$HOME/.config/qtile"
qtile check -c "$HOME/.config/qtile/config.py"
sh -n "$HOME/.config/qtile/autostart.sh"
sh -n "$HOME/.config/qtile/scripts/power-menu.sh"
find "$HOME/.config/fish" -type f -name '*.fish' -exec fish -n {} \;
python -m json.tool "$HOME/.config/fastfetch/config.jsonc" > /dev/null
fastfetch -c "$HOME/.config/fastfetch/config.jsonc" --show-errors
python -c 'import pathlib,tomllib; p=pathlib.Path.home()/".config/alacritty"; [tomllib.loads(f.read_text()) for f in p.rglob("*.toml")]; print("TOML OK")'
~~~

Abre una ventana de Alacritty para comprobar fuente y renderizado. **No se ha validado el inicio real de Qtile ni el driver NVIDIA en el equipo**. Si algo falla, restaura las carpetas ~/.config/NOMBRE.backup.FECHA desde una TTY. La sintaxis correcta no garantiza el funcionamiento gráfico.

## Mantenimiento

- Tema: qtile/themes/obsidian.json, alacritty/themes/obsidian.toml, fish/conf.d/obsidian.fish y fastfetch/config.jsonc.
- Barra, layouts, grupos, atajos: qtile/settings/.
- Compositor, notificaciones, red, USB y fondo: qtile/autostart.sh; archivos separados en picom/, dunst/ y rofi/. No duplicar servicios en .xprofile.
- Fish genera fish_variables por máquina; se ignora en Git.
- Bash es opcional: Alacritty inicia Fish directamente.
- La captura anterior se ha retirado por no representar Obsidian. Añade una captura real al documentar el escritorio.

## Documentación oficial

[Qtile: instalación](https://docs.qtile.org/en/stable/manual/install/) · [Qtile: widgets](https://docs.qtile.org/en/stable/manual/ref/widgets.html) · [Fish: prompt](https://fishshell.com/docs/current/prompt.html) · [Alacritty: TOML](https://alacritty.org/config-alacritty.html) · [Fastfetch: configuración JSONC](https://github.com/fastfetch-cli/fastfetch/wiki/Configuration) · [Rofi: temas](https://davatorium.github.io/rofi/current/rofi-theme.5/) · [Dunst: documentación](https://dunst-project.org/documentation/) · [Picom: opciones](https://picom.app/)

Este repositorio no incluye un archivo LICENSE; no debe presentarse como licenciado bajo MIT.
