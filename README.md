# Arch Linux · Qtile Operator HUD

Configuración de **Arch Linux + Qtile (X11) + Alacritty + Fish + Fastfetch + Rofi + Dunst + Picom**, con interfaz **Operator HUD**: productividad orientada al teclado, barra de información contextual, espacios de trabajo semánticos y terminal desplegable, optimizada para ultrawide. Tres temas intercambiables — **Obsidian** (grafito y verde azulado), **Cyberpunk** (grafito profundo, cian y magenta) y **Darcula** (gris JetBrains, naranja y verde)— en los componentes del escritorio.

> Repositorio de dotfiles, no instalador de Arch Linux. No configura drivers NVIDIA, cifrado, display manager, red ni hardening. **Solo Qtile sobre X11**: utiliza xrandr, picom, feh y Systray, no Qtile Wayland.

## Estructura

| Ruta | Función |
| --- | --- |
| .config/qtile/config.py | Configuración principal y hook startup_once |
| .config/qtile/settings/ | Atajos, grupos, layouts, widgets, pantallas, ratón y tema |
| .config/qtile/themes/{obsidian,cyberpunk,darcula}.json | Paletas de Qtile |
| .config/qtile/autostart.sh | Inicio de servicios, red, USB y fondo |
| .config/qtile/scripts/theme-switch.py | Selector seguro y atómico de tema |
| .config/qtile/scripts/theme-menu.sh | Menú gráfico Rofi de temas |
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

Qtile: barra **Operator HUD de 44 px**, espacios **01 DEV, 02 WEB, 03 DATA, 04 OPS, 05 LAB, 06 COMMS, 07 DOCS y 08 MISC**, lista de ventanas con foco, layout activo, CPU, RAM, red y reloj; layouts MonadTall (principal), Columns, Bsp, MonadWide y Max, con márgenes de 12 px y foco de 2 px. El widget Net suma las interfaces activas; sin Wi-Fi fijada ni batería.

Alacritty: JetBrainsMono Nerd Font a 12,5 puntos, 0,97 de opacidad, TOML y Fish. Fish: prompt nativo de dos líneas, Git, Python venv, códigos de error, duración y hora. Fastfetch se ejecuta con `sys` y, opcionalmente, al iniciar Fish. No se ejecuta automáticamente por defecto. Cada tema dispone de perfiles versionados para los componentes; el selector sincroniza los archivos activos. Si modificas una paleta, actualiza el perfil de cada aplicación correspondiente.

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
sudo pacman -S --needed eza zoxide brightnessctl btop
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

Cada tema incluye un SVG de 3440 × 1440 en `.config/qtile/wallpapers/`. El script `wallpaper.sh` convierte el tema seleccionado a PNG en `~/.cache/qtile-wallpapers/` y lo aplica con `feh`. En ausencia de conversor o imagen, se utiliza el color sólido de cada tema.

## Atajos principales

Super es la tecla Windows/Super.

| Atajo | Acción |
| --- | --- |
| Super + Enter | Alacritty + Fish |
| Super + ` | Terminal scratchpad desplegable |
| Super + Shift + ` | Panel btop desplegable (requiere btop) |
| Super + p | Menú Operator HUD con acciones rápidas |
| Super + f | Alternar pantalla completa |
| Super + Shift + Espacio | Alternar ventana flotante |
| Super + [ / ] | Grupo anterior / siguiente |
| Super + Escape | Volver al grupo anterior |
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
| Super + Shift + p | Menú de energía |
| Super + Shift + t | Selector de temas (Obsidian, Cyberpunk, Darcula) |
| Super + Shift + n | Recuperar notificación anterior (Dunst) |
| Super + s / Super + Shift + s | Captura completa / selección |
| Super + Ctrl + r | Recargar Qtile |
| Super + Ctrl + q | Salir de Qtile |
| Super + r | Ejecutar comando mediante Rofi |

Super + r abre el comando integrado de Qtile. Los demás atajos de apps están en .config/qtile/settings/keys.py.

## Operator HUD · arquitectura de interacción

El diseño **Operator HUD** se basa en los componentes nativos `ScratchPad`, `DropDown`, `GroupBox`, `TaskList` y `CurrentLayout` de Qtile. No es un tema de colores ni un widget pack externo: modifica el modelo de interacción del escritorio.

- **Barra flotante modular (44 px)**: acceso al menú de operador, escritorios semánticos, layout actual, selector interactivo de ventanas, métricas de CPU/RAM/red y zona de notificaciones, temas y energía. La lista de ventanas destaca la enfocada y permite activarlas mediante clic.
- **Diseño ultrawide**: `MonadTall` con proporción 0,57 para separar editor y herramientas; `Columns` proporciona tres columnas de trabajo y `Bsp` particiones flexibles. `Max` permite concentración sin eliminar las ventanas.
- **Scratchpad terminal**: `Super + \`` despliega Alacritty sobre el grupo actual; se oculta al perder foco. `Super + Shift + \`` abre una segunda terminal flotante con `btop` (opcional).
- **Menú de operador**: `Super + P` abre un menú Rofi de acciones permitidas: aplicaciones, ventanas, terminal, monitorización, archivos, cambio de tema, historial de notificaciones, comandos y energía.
- **Pantallas secundarias**: la barra utiliza una disposición reducida por debajo de 1800 píxeles, preservando grupos, reloj y controles básicos. Cada monitor construye sus propias instancias de widgets.
- **Compatibilidad**: los atajos existentes de aplicaciones, capturas y gestión de temas siguen disponibles. Cyberpunk, Darcula y Obsidian mantienen la misma estructura y solo alteran colores/fondo.
- **Privacidad**: el menú de operador no ejecuta instrucciones suministradas por el usuario. La opción explícita «Comando» utiliza el lanzador Rofi existente y debe tratarse como una interfaz para ejecutar comandos voluntariamente.

Para una instalación completa de monitorización opcional:

~~~bash
sudo pacman -S --needed btop
~~~

El panel btop no aparece automáticamente ni añade un daemon en segundo plano; se crea cuando se invoca su atajo.

## Escritorio Obsidian · fase 1

- **Rofi** (`.config/rofi/`): lanzador de aplicaciones (`Super+m`), selector de ventanas (`Super+Shift+m`) y tema Rasi de 720 px con búsqueda central, iconos Papirus-Dark y selección discreta.
- **Dunst** (`.config/dunst/dunstrc`): notificaciones en la pantalla enfocada, esquinas redondeadas, separación de 9 px, barra de progreso y urgencias codificadas con el color de alerta.
- **Picom** (`.config/picom/picom.conf`): backend GLX, VSync, sombras suaves y esquinas de 9 px, sin blur ni transparencias forzadas. La composición depende del driver y puede requerir ajustes en NVIDIA.
- **Fondo Obsidian** (`.config/qtile/wallpapers/obsidian.svg`): vector editable y reproducible; `rsvg-convert` genera una imagen de 3440 × 1440 una sola vez o cuando cambia el SVG. Sin descargas ni dependencias externas durante el arranque.
- **Menú de energía** (`Super+Shift+p`): bloquear, suspender, cerrar sesión, reiniciar o apagar. Exige confirmación para acciones disruptivas y **no ejecuta entradas arbitrarias**. El bloqueo de sesión usa i3lock; xss-lock garantiza que se invoque al suspender mediante logind.
- **Barra Qtile**: botón de energía al extremo derecho que abre el mismo menú.

Para probar Dunst: `dunstify "Obsidian" "Notificación de prueba"`. Para probar Rofi: `rofi -show drun`. Para probar Picom: `picom --config ~/.config/picom/picom.conf` (si ya hay otro compositor activo, no ejecutes una segunda instancia).

**Seguridad del bloqueo:** el menú suspende únicamente si detecta xss-lock e i3lock activos. Antes de depender de esta opción, comprueba desde una sesión real que i3lock bloquea y que al reanudar exige autenticación. Este bloqueo es funcional, pero no constituye todavía un tema personalizado de pantalla de bloqueo (fase 2). Los mecanismos de suspensión de otras aplicaciones o de la BIOS no quedan cubiertos por este menú.

## Selección de temas (escritorio completo)

Tres perfiles predefinidos:

| Tema | Fondo | Acento | Carácter |
| --- | --- | --- | --- |
| Obsidian | `#111820` | `#82CDBE` | Minimalista y profesional (predeterminado) |
| Cyberpunk | `#0B101B` | `#FF4FA3` | Neón controlado con detalles cian |
| Darcula | `#2B2B2B` | `#CC7832` | Inspiración JetBrains, contraste cálido |

**Con Rofi**: `Super + Shift + T` o el botón de tema en la barra superior. El selector ofrece los tres nombres; cancelar no modifica nada.

**Desde la terminal**:

~~~bash
python ~/.config/qtile/scripts/theme-switch.py --list
python ~/.config/qtile/scripts/theme-switch.py --current
python ~/.config/qtile/scripts/theme-switch.py cyberpunk
python ~/.config/qtile/scripts/theme-switch.py darcula
python ~/.config/qtile/scripts/theme-switch.py obsidian
~~~

Para cambiar sin recargar Qtile y los servicios gráficos (por ejemplo, desde TTY):

~~~bash
python ~/.config/qtile/scripts/theme-switch.py darcula --no-reload
~~~

**Alcance del cambio**: Qtile (incluidos widgets/bordes), Alacritty (ANSI), Fish (sintaxis y prompts en nuevas sesiones), Fastfetch, Rofi, Dunst, Picom y wallpaper. Se conservan los atajos, layouts, parámetros de privacidad y estructura de módulos. **No cambia el tema GTK de aplicaciones externas** ni los estilos de páginas web.

Los perfiles fuente están en `themes/<tema>.*` dentro de cada componente y los archivos activos tienen nombres estables: `alacritty/themes/active.toml`, `rofi/themes/active.rasi`, `fish/conf.d/theme.fish`, `fastfetch/config.jsonc`, `dunst/dunstrc` y `picom/picom.conf`. Qtile usa `qtile/config.json`.

El selector valida que existan los perfiles y después sustituye los archivos activos con escritura temporal y reemplazo atómico por archivo. **No es una transacción global** ante un corte de energía: ejecutar otra vez el selector corrige una actualización parcial. En una sesión X11 intenta actualizar fondo, Dunst, Picom y Qtile. Fish aplica los cambios en nuevas terminales; Alacritty dispone de recarga automática. La configuración de respaldo `.bashrc` también selecciona el acento del tema al iniciar una nueva sesión Bash. Si un servicio no permite recarga en tu versión, reinicia la sesión. El tema seleccionado se mantiene entre reinicios.

Tras desplegar por primera vez, ejecuta el selector con el tema activo para sincronizar los perfiles:

~~~bash
python ~/.config/qtile/scripts/theme-switch.py obsidian --no-reload
~~~

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
sh -n "$HOME/.config/qtile/scripts/wallpaper.sh"
sh -n "$HOME/.config/qtile/scripts/theme-menu.sh"
sh -n "$HOME/.config/qtile/scripts/operator-menu.sh"
python -m py_compile "$HOME/.config/qtile/scripts/theme-switch.py"
python -m unittest discover -s tests -v
find "$HOME/.config/fish" -type f -name '*.fish' -exec fish -n {} \;
python -m json.tool "$HOME/.config/fastfetch/config.jsonc" > /dev/null
fastfetch -c "$HOME/.config/fastfetch/config.jsonc" --show-errors
python -c 'import pathlib,tomllib; p=pathlib.Path.home()/".config/alacritty"; [tomllib.loads(f.read_text()) for f in p.rglob("*.toml")]; print("TOML OK")'
~~~

Abre una ventana de Alacritty para comprobar fuente y renderizado. **No se ha validado el inicio real de Qtile ni el driver NVIDIA en el equipo**. Si algo falla, restaura las carpetas ~/.config/NOMBRE.backup.FECHA desde una TTY. La sintaxis correcta no garantiza el funcionamiento gráfico.

## Mantenimiento

- Temas: modifica los perfiles de `qtile/themes/`, `alacritty/themes/`, `fish/themes/`, `fastfetch/themes/`, `rofi/themes/`, `dunst/themes/` y `picom/themes/`; aplica con `theme-switch.py`.
- Barra, layouts, grupos, atajos: qtile/settings/.
- Compositor, notificaciones, red, USB y fondo: qtile/autostart.sh; archivos separados en picom/, dunst/ y rofi/. No duplicar servicios en .xprofile.
- Fish genera fish_variables por máquina; se ignora en Git.
- Bash es opcional: Alacritty inicia Fish directamente.
- La captura anterior se ha retirado por no representar Obsidian. Añade una captura real al documentar el escritorio.

## Documentación oficial

[Qtile: instalación](https://docs.qtile.org/en/stable/manual/install/) · [Qtile: grupos y ScratchPad](https://docs.qtile.org/en/stable/manual/config/groups.html) · [Qtile: widgets](https://docs.qtile.org/en/stable/manual/ref/widgets.html) · [Fish: prompt](https://fishshell.com/docs/current/prompt.html) · [Alacritty: TOML](https://alacritty.org/config-alacritty.html) · [Fastfetch: configuración JSONC](https://github.com/fastfetch-cli/fastfetch/wiki/Configuration) · [Rofi: temas](https://davatorium.github.io/rofi/current/rofi-theme.5/) · [Dunst: documentación](https://dunst-project.org/documentation/) · [Picom: opciones](https://picom.app/)

Las comprobaciones de coherencia de los tres perfiles se ejecutan también en GitHub Actions para cada pull request. Esto no sustituye las pruebas de renderizado en una sesión X11 real.

Este repositorio no incluye un archivo LICENSE; no debe presentarse como licenciado bajo MIT.

