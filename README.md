# Arch Linux · Qtile Operator HUD

Entorno de escritorio **Qtile sobre X11** para Arch Linux: navegación por teclado, barra contextual, espacios de trabajo semánticos y terminal desplegable. Incluye **Alacritty, Fish, Fastfetch, Rofi, Dunst, Picom, monitorización opcional, bloqueo i3lock/xss-lock y tema de acceso SDDM Qt6**. Dispone de tres temas coordinados: **Obsidian** (predeterminado), **Cyberpunk** y **Darcula**.

**Alcance.** Es un repositorio de dotfiles y un instalador de configuraciones de usuario, **no una imagen ni instalador de Arch Linux**. Se parte de Arch ya instalado, con usuario no root y acceso a Internet. No instala ni configura LUKS2, particiones, firmware, Secure Boot, drivers NVIDIA, firewalls ni reglas PAM. La sesión está diseñada para **X11**, no para Qtile Wayland.

## 0. Antes de comenzar

Comprueba en una TTY o en el escritorio actual:

~~~bash
id -un
uname -r
systemctl --version
command -v sudo
command -v pacman
~~~

Necesitas una cuenta con acceso administrativo mediante sudo, conexión a Internet y un servidor Xorg funcional. Si usas NVIDIA, **instala previamente el controlador adecuado para tu GPU y el kernel instalado** siguiendo la documentación de Arch; no instales un paquete NVIDIA a ciegas. Comprueba que Xorg funciona antes de cambiar de gestor de acceso. La configuración utiliza Picom con GLX; si detectas artefactos, deshabilita Picom temporalmente para diagnosticar el driver.

No elimines tu sesión de escritorio anterior ni su gestor de acceso hasta terminar las pruebas. Mantén disponible una TTY (normalmente **Ctrl+Alt+F3**) y una contraseña de usuario funcional. Si utilizas cifrado del disco, conserva también el procedimiento de recuperación LUKS.

> Los bloques de comandos de esta guía están escritos en **POSIX sh/Bash**. Desde Fish ejecuta los scripts con **sh**; no pegues bucles Bash directamente en la consola Fish.

## 1. Instalar los paquetes de Arch Linux

Actualiza primero los repositorios y el sistema:

~~~bash
sudo pacman -Syu
~~~

### 1.1 Base gráfica y herramientas del proyecto

~~~bash
sudo pacman -S --needed \
  git python sudo qtile python-psutil \
  xorg-server xorg-xauth xorg-xinit xorg-xrandr xorg-xset xorg-xsetroot \
  alacritty fish fastfetch rofi picom dunst \
  ttf-jetbrains-mono-nerd noto-fonts papirus-icon-theme \
  librsvg feh scrot thunar thunar-volman gvfs udisks2 udiskie \
  networkmanager network-manager-applet \
  i3lock xss-lock \
  lxqt-policykit polkit \
  procps-ng pacman-contrib
~~~

**Qué instala:** Qtile (gestor de ventanas X11), Alacritty/Fish, lanzadores y notificaciones, composición, fondos, gestor de archivos y unidades USB, NetworkManager, fuentes, bloqueo y agente gráfico Polkit. El paquete **xorg-xset** es necesario para ejecutar el temporizador de inactividad \`xset s 600 600\`. **libpulse**, incluido con los componentes de audio correspondientes, aporta \`pactl\` para los atajos de volumen.

Para audio mediante PipeWire, solo si aún no tienes un sistema de audio configurado:

~~~bash
sudo pacman -S --needed pipewire pipewire-audio pipewire-pulse wireplumber libpulse
~~~

No instales dos servidores de audio alternativos si ya utilizas PulseAudio o una configuración PipeWire existente. Comprueba el resultado en la sesión iniciada con \`pactl info\` y \`wpctl status\`. Los atajos de volumen necesitan un servidor PulseAudio compatible.

Opcionales según uso:

~~~bash
sudo pacman -S --needed btop eza zoxide brightnessctl
~~~

El panel desplegable de monitorización utiliza **btop**; las otras utilidades enriquecen Fish o gestionan el brillo cuando el hardware lo permite. Firefox, VS Code, Android Studio, GIMP, LibreOffice, qBittorrent y otras apps tienen atajos definidos, pero **no se instalan automáticamente**.

### 1.2 Servicios necesarios

Si esta instalación utiliza NetworkManager, comprueba su estado:

~~~bash
systemctl status NetworkManager.service
~~~

Si no estaba habilitado y has elegido NetworkManager como gestor de red:

~~~bash
sudo systemctl enable --now NetworkManager.service
~~~

**No hagas esto en remoto sin confirmar la configuración de red**, ni mantengas dos servicios que intenten administrar la misma interfaz. No es necesario activar manualmente un servicio systemd para Picom, Dunst, Fish, Fastfetch o el agente Polkit: Qtile los inicia cuando corresponde.

Para dispositivos USB, comprueba que el servicio y el montaje funcionan después de iniciar Qtile; udiskie utiliza UDisks2 y la autorización Polkit. No ejecutes udiskie como root.

## 2. Clonar y comprobar el repositorio

~~~bash
git clone https://github.com/mier48/arch-qtile-config.git
cd arch-qtile-config
~~~

Antes de modificar el equipo, ejecuta el comprobador. **Es compatible con Bash y Fish** porque se invoca explícitamente con sh:

~~~bash
sh scripts/install-dotfiles.sh --check
~~~

El comprobador verifica las herramientas principales y ejecuta las pruebas estáticas. También puedes ejecutar:

~~~bash
python -m unittest discover -s tests -v
python -m compileall -q .config/qtile
sh -n scripts/install-dotfiles.sh
sh -n sddm/install-theme.sh
~~~

Si aparece un fallo, resuélvelo **antes de instalar**. Las pruebas estáticas no validan el comportamiento real del escritorio, la carga del greeter QML, ni los drivers.

## 3. Instalar los dotfiles (con copia de seguridad)

**No uses sudo** en este paso. El instalador copia exactamente los siete directorios \`qtile\`, \`fish\`, \`alacritty\`, \`fastfetch\`, \`rofi\`, \`dunst\` y \`picom\` a **~/.config/**; no toca GTK, cuentas, PAM ni SDDM.

~~~bash
sh scripts/install-dotfiles.sh --apply --theme obsidian
~~~

Sustituye **obsidian** por **cyberpunk** o **darcula** si deseas otro perfil inicial. Si omites \`--theme\`, conserva el tema válido previamente seleccionado o utiliza Obsidian en una instalación nueva.

El instalador:

1. Comprueba los tests y la presencia de todos los directorios de origen.
2. Prepara los archivos en una carpeta temporal dentro de ~/.config.
3. Renombra los originales como **~/.config/NOMBRE.backup.FECHA-PID**.
4. Instala los nuevos directorios y sincroniza los colores del tema mediante el selector existente.
5. Intenta restaurar los directorios anteriores si ocurre un error durante el despliegue.

El respaldo es local, **no una copia externa**. Una interrupción brusca del suministro eléctrico no garantiza una transacción global entre directorios. Conserva tus copias hasta verificar un reinicio completo; no se modifican los archivos personales de otros programas.

Valida la configuración instalada:

~~~bash
qtile check -c "$HOME/.config/qtile/config.py"
sh -n "$HOME/.config/qtile/autostart.sh"
sh -n "$HOME/.config/qtile/scripts/lock.sh"
sh -n "$HOME/.config/qtile/scripts/power-menu.sh"
fish -n "$HOME/.config/fish/config.fish"
python -m json.tool "$HOME/.config/fastfetch/config.jsonc" >/dev/null
~~~

**No recargues Qtile si \`qtile check\` falla**. Abre una TTY y restaura el respaldo de Qtile si la sesión gráfica deja de funcionar.

## 4. Elegir la forma de iniciar Qtile

Hay dos alternativas: **SDDM (recomendada)** o **startx**. No necesitas ambas y no debes iniciar una segunda sesión X sobre una sesión gráfica ya existente.

### Opción A: SDDM Qt6

Instala los componentes de SDDM:

~~~bash
sudo pacman -S --needed sddm qt6-declarative qt6-svg
~~~

Instala el tema personalizado desde la raíz del repositorio (operación privilegiada, **separada** de los dotfiles):

~~~bash
sudo sh sddm/install-theme.sh obsidian
~~~

El instalador admite también **cyberpunk** y **darcula**. Crea una variante del tema en **/usr/share/sddm/themes/operator-NOMBRE/** y el override **/etc/sddm.conf.d/90-operator-hud.conf**. Hace copias si existen versiones anteriores. **No modifica /etc/pam.d/, no configura autologin, no habilita servicios y no cambia el display manager vigente.**

Prueba primero el tema mediante el greeter de tu versión de SDDM:

~~~bash
command -v sddm-greeter-qt6
pacman -Ql sddm | grep '/sddm-greeter'
~~~

En Arch Linux, el ejecutable Qt6 está en \`/usr/bin/sddm-greeter-qt6\`. Prueba su opción **--test-mode** con la ruta del tema instalado:

~~~bash
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/operator-obsidian
~~~

Comprueba la ruta disponible en tu versión y utiliza \`--help\` si difiere. Si has instalado otra variante, ajusta **operator-obsidian** al nombre correspondiente. El modo de prueba **no autentica realmente contra PAM**.

Antes de habilitar SDDM, inspecciona el gestor de acceso actual:

~~~bash
systemctl status display-manager.service
ls -l /etc/systemd/system/display-manager.service
ls /usr/share/xsessions/
~~~

Asegúrate de disponer de una sesión **Qtile X11** registrada entre las sesiones instaladas. Si ya hay GDM, LightDM u otro display manager, desactívalo por el procedimiento de Arch antes de activar SDDM; **no habilites dos gestores de acceso simultáneamente**.

Cuando hayas probado el greeter, conserves una TTY de rescate y no haya un gestor en conflicto:

~~~bash
sudo systemctl enable sddm.service
sudo reboot
~~~

En el greeter selecciona **Qtile X11**, introduce usuario y contraseña y comprueba el acceso. No hace falta establecer un inicio de sesión automático; la autenticación la gestiona SDDM mediante PAM.

Consulta también **[sddm/README.md](sddm/README.md)** para el alcance, cambio de temas y recuperación del greeter.

### Opción B: startx (sin SDDM)

Si prefieres iniciar Qtile desde una TTY, mantén SDDM deshabilitado, utiliza **xorg-xinit** y crea una copia inicial de los scripts de Xorg:

~~~bash
cp /etc/X11/xinit/xinitrc "$HOME/.xinitrc"
~~~

Edita **~/.xinitrc** conservando el bloque que ejecuta **/etc/X11/xinit/xinitrc.d/**, pero **sustituye las aplicaciones finales de ejemplo (twm/xclock/xterm) por una única instrucción de inicio**:

~~~sh
exec qtile start
~~~

Si ya tenías ~/.xinitrc, **no lo sobrescribas**: revisa primero su contenido. Desde la TTY del usuario:

~~~bash
startx
~~~

Para reforzar el aislamiento, ArchWiki recomienda lanzar Xorg desde la misma consola virtual de inicio de sesión y no escuchar conexiones TCP. Revisa la opción de ~/.xserverrc documentada en ArchWiki antes de personalizarla. Comprueba que DBus y systemd-logind detectan la sesión correctamente.

## 5. Comprobar el escritorio y los periféricos

Una vez iniciada la sesión gráfica:

~~~bash
echo "$XDG_SESSION_TYPE"
xrandr --listmonitors
qtile cmd-obj -o cmd -f status
pgrep -a picom
pgrep -a dunst
pgrep -a xss-lock
pgrep -af lxqt-policykit-agent
pactl info
~~~

**Resultado esperado:** sesión \`x11\`, monitor/es detectados, Qtile activo, una instancia por servicio gráfico necesario, agente Polkit disponible y audio funcional. Para solucionar problemas con NVIDIA, consulta primero los registros de Xorg/SDDM y las instrucciones oficiales del driver.

Comprueba manualmente los componentes: Rofi con **Super+M**, terminal **Super+Enter**, ScratchPad **Super+tecla grave**, barra Operator HUD, notificaciones con \`dunstify "Prueba" "Notificación"\`, Thunar y montaje de un USB. El panel btop utiliza **Super+Shift+tecla grave** si has instalado btop.

### Temas

El selector integrado permite cambiar **Obsidian / Cyberpunk / Darcula** con **Super+Shift+T** o desde terminal:

~~~bash
python "$HOME/.config/qtile/scripts/theme-switch.py" --list
python "$HOME/.config/qtile/scripts/theme-switch.py" --current
python "$HOME/.config/qtile/scripts/theme-switch.py" cyberpunk
~~~

Este selector actualiza Qtile, Alacritty, Fish, Fastfetch, Rofi, Dunst, Picom y wallpaper. Fish aplica la nueva configuración en terminales nuevas; algunas aplicaciones necesitan reiniciarse.

**El tema de SDDM es una configuración privilegiada independiente**. Cambiar el tema del usuario no actualiza automáticamente SDDM. Para cambiarlo, vuelve a ejecutar el instalador SDDM con sudo tras probar la nueva variante.

## SDDM Cyberpunk y Fastfetch en Fish

Si el escritorio está en Cyberpunk pero SDDM aparece en Obsidian, recuerda que el greeter es independiente del tema de usuario. Tras instalar la versión actualizada del repositorio, desde su raíz ejecuta:

~~~bash
sudo sh sddm/install-theme.sh cyberpunk
# O selecciona expresamente el mismo tema que tiene Qtile:
sudo sh sddm/install-theme.sh --from-qtile
sh sddm/install-theme.sh --current
~~~

El script instala una variante de `operator-hud` con el `theme.conf` correcto (sección `[General]`), establece la opción `[Theme] Current` y avisa si encuentra posibles overrides. Puedes probar Cyberpunk con:

~~~bash
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/operator-cyberpunk
~~~

No se modifican las reglas PAM ni se habilitan servicios automáticamente. Consulta [sddm/README.md](sddm/README.md) si el greeter sigue mostrando el tema anterior.

**Fastfetch** ahora se ejecuta automáticamente en terminales Fish interactivas locales, excepto sesiones SSH y shells secundarios que ya lo mostraron. No se ejecuta en Fish no interactivo. Para desactivarlo:

~~~fish
set -U FASTFETCH_AUTOSTART 0
~~~

Para volver a activarlo:

~~~fish
set -U FASTFETCH_AUTOSTART 1
~~~

El acceso rápido `sys` sigue disponible cuando Fastfetch está instalado. Tras actualizar `~/.config/fish/config.fish`, abre una nueva terminal Alacritty para comprobar el arranque.

## 6. Bloqueo, suspensión y autenticación

La pantalla de bloqueo protege una sesión que **ya está abierta**; SDDM se limita al inicio de sesión. No compartas ni sustituyas sus mecanismos de autenticación.

- **i3lock** utiliza la pila PAM del sistema para desbloquear; el repositorio no instala un módulo PAM propio ni guarda contraseñas.
- **xss-lock** supervisa la inactividad X11 y coordina con **systemd-logind** las suspensiones mediante \`--transfer-sleep-lock\`.
- **lock.sh** usa una imagen estática por tema, nunca una captura de pantalla con datos privados. Ejecuta i3lock en primer plano (\`-n\`) y recurre a un fondo sólido si falla el SVG.
- **xset s 600 600** establece unos diez minutos de inactividad X11. No sustituye una política corporativa de bloqueo.
- El menú de energía comprueba la presencia de los mecanismos de bloqueo antes de permitir la suspensión desde ese menú. No puede garantizar el bloqueo ante todos los eventos externos, fallos de X11, suspensión del firmware ni condiciones de carrera.

Prueba primero bloqueo y desbloqueo manual:

~~~bash
sh "$HOME/.config/qtile/scripts/lock.sh"
~~~

A continuación, valida el bloqueo automático después de diez minutos sin actividad y finalmente una suspensión/reanudación **con una persona presente en el equipo**. Comprueba que se solicita credencial antes de poder interactuar con las ventanas. Si la prueba falla, **no des por segura la suspensión**. Puedes consultar:

~~~bash
loginctl session-status
systemd-inhibit --list
journalctl -b --no-pager -n 100
~~~

Para hibernación hacen falta configuración de swap, reanudación e initramfs; **no está implementada aquí**. Un bloqueo de pantalla tampoco cifra la memoria RAM ni sustituye LUKS2.

## Diagnóstico: Firefox abre, pero no responde a clics o teclado

La política de foco de Qtile es `focus_on_window_activation = "smart"`: Firefox puede solicitar foco si está en el grupo visible. Las ventanas flotantes se mantienen por encima y un clic las trae al frente; los escritorios y layouts originales se conservan. **No se ha identificado todavía una causa única del problema**: hay que distinguir foco incorrecto, compositor y fallo interno de Firefox.

### Aislamiento sin modificar archivos

**1. Comprueba el compositor.** Con Firefox abierto, ejecuta:

~~~bash
pkill -x picom
~~~

Si Firefox vuelve a responder, el origen probable está en Picom/GLX/driver y no en las reglas de Qtile. Puedes probar la sesión sin compositor y revisar `picom --log-level=debug --config ~/.config/picom/picom.conf` desde una terminal, con una sola instancia activa. No desactives la aceleración de Firefox ni fuerces variables de entorno de X11/Wayland sin antes aislar esta causa.

**2. Comprueba el foco.** Abre una terminal, ejecuta:

~~~bash
xprop -root _NET_ACTIVE_WINDOW
xprop WM_CLASS
~~~

El segundo comando te permitirá seleccionar visualmente una ventana de Firefox. Si falta `xprop`, instálalo mediante `sudo pacman -S --needed xorg-xprop`. También puedes consultar `qtile cmd-obj -o window -f info` según la versión instalada.

**3. Comprueba Firefox sin perfil habitual**, solo para diagnosticar:

~~~bash
firefox --ProfileManager
~~~

Crea un perfil temporal de prueba sin modificar el habitual; evita ejecutar dos instancias con el mismo perfil a la vez. Si el navegador funciona con un perfil nuevo, revisa extensiones, preferencias y aceleración de Firefox antes de atribuir el problema a Qtile.

**4. Comprueba registros y versión:**

~~~bash
qtile --version
pacman -Q firefox qtile picom
journalctl --user -b --no-pager -n 100
~~~

Reinicia Qtile con **Super+Ctrl+R** tras aplicar un cambio de configuración validado con `qtile check -c ~/.config/qtile/config.py`. El valor `focus_on_window_activation = "smart"` mejora la gestión de activación de ventanas, pero **no puede resolver un proceso de Firefox congelado ni un fallo de renderizado de NVIDIA**.

## Fastfetch · Operator HUD (estética Neofetch)

Fastfetch reproduce la disposición clásica de **Neofetch** sin sus limitaciones de mantenimiento: **logo ASCII completo de Arch a la izquierda** y resumen del equipo a la derecha, con título `usuario@equipo`, separación horizontal, claves con símbolos Nerd Font, columna de datos alineada y una barra de utilización de RAM. Se han eliminado los tres encabezados numerados anteriores.

Los datos de sistema, kernel, host, tiempo encendido, paquetes, gestor de ventanas, terminal, shell, pantalla, CPU, GPU, RAM y disco se **detectan en tiempo real**: no se fijan valores concretos de hardware. No se hacen consultas de red ni se imprime la IP local o pública.

Existen tres perfiles completos:

- **Obsidian:** `.config/fastfetch/themes/obsidian.jsonc`
- **Cyberpunk:** `.config/fastfetch/themes/cyberpunk.jsonc`
- **Darcula:** `.config/fastfetch/themes/darcula.jsonc`

El archivo `~/.config/fastfetch/config.jsonc` contiene la variante actualmente activa; el selector `Super+Shift+T` lo sincroniza con el resto de aplicaciones.

Para previsualizar y diagnosticar:

~~~bash
fastfetch
fastfetch --config ~/.config/fastfetch/themes/cyberpunk.jsonc
fastfetch --config ~/.config/fastfetch/themes/darcula.jsonc
python -m json.tool ~/.config/fastfetch/config.jsonc >/dev/null
~~~

En Fish, `sys` se expande a `fastfetch`. Por defecto la configuración actual de Fish muestra Fastfetch una vez al abrir una sesión local interactiva; para desactivarlo:

~~~fish
set -U FASTFETCH_AUTOSTART 0
~~~

Para volver a activarlo: `set -U FASTFETCH_AUTOSTART 1`. No se ejecuta automáticamente en SSH y se evita repetirlo en shells Fish anidados. El logo completo ocupa más columnas que el anterior: se recomienda una terminal de **al menos 90 columnas**. Si el equipo usa un terminal estrecho, reduce el ancho de fuente o utiliza un modo compacto temporal (`fastfetch --logo-type small`).

## Selector WireGuard en Qtile

En la parte derecha de la barra **Operator HUD** hay un **icono permanente de VPN (`󰖂`) inmediatamente al lado del selector de temas (`󰔎`)**. **Haz clic izquierdo en el icono VPN** para abrir directamente el selector Rofi de WireGuard, igual que haces con el icono de temas. No se muestra ningún texto de estado junto al icono y no se realizan consultas periódicas desde la barra. Se mantienen **Super+Shift+V** y **Super+P → WireGuard** como accesos alternativos.

El menú lista **exclusivamente conexiones nativas WireGuard gestionadas por NetworkManager** (`TYPE=wireguard`). Un círculo relleno marca cada perfil activo. Selecciona uno inactivo para conectarlo o uno activo para desconectarlo. Las operaciones usan el **UUID** completo, no el nombre del perfil; no ejecutan una shell ni muestran claves privadas. NetworkManager y Polkit gestionan permisos y secretos.

### Importar un túnel WireGuard existente

NetworkManager dispone de soporte nativo para WireGuard: **no necesitas OpenVPN ni `networkmanager-openvpn`**. Si tienes un archivo de configuración de WireGuard (por ejemplo `~/vpn/mi-tunel.conf`), impórtalo así:

~~~bash
sudo pacman -S --needed wireguard-tools networkmanager
nmcli connection import type wireguard file "$HOME/vpn/mi-tunel.conf"
nmcli -f NAME,UUID,TYPE connection show
~~~

El archivo `.conf` contiene habitualmente la clave privada del cliente. Protégelo con permisos restrictivos, no lo subas al repositorio ni lo expongas en registros. Tras verificar que la conexión importada funciona, elimina las copias que ya no necesites siguiendo tu política de gestión de secretos.

**Importante:** si levantas tus túneles con `wg-quick up` o `wg-quick@nombre.service`, esos túneles **no se controlan con este selector**. Debes elegir un único gestor para cada interfaz: importa la configuración en NetworkManager y evita mantener simultáneamente `wg-quick` sobre el mismo túnel. El indicador `WG/NM OFF` solo significa que **NetworkManager no tiene ningún perfil WireGuard activo**, no que el equipo carezca de otros túneles.

### Diagnóstico y límites de seguridad

~~~bash
nmcli -f NAME,UUID,TYPE connection show
nmcli -f NAME,UUID,TYPE connection show --active
python "$HOME/.config/qtile/scripts/vpn-menu.py" --status
python "$HOME/.config/qtile/scripts/vpn-menu.py"
sudo wg show
~~~

`wg show` permite inspeccionar túneles del kernel, incluidos los ajenos a NetworkManager, pero no se usa para modificarlos desde este menú.

**WG/NM ON no garantiza privacidad ni anonimato.** No valida la IP de salida, la tabla de rutas, DNS, fugas IPv6 ni un kill switch. Una desconexión puede devolver el tráfico a la red normal. Si necesitas bloquear todo tráfico fuera del túnel, implementa y comprueba una política de firewall/killswitch independiente antes de utilizarlo.

## 7. Actualizaciones

Desde la raíz del clon local:

~~~bash
git pull --ff-only origin main
python -m unittest discover -s tests -v
sh scripts/install-dotfiles.sh --check
sh scripts/install-dotfiles.sh --apply
qtile check -c "$HOME/.config/qtile/config.py"
~~~

El instalador vuelve a crear respaldos y mantiene el tema anterior. **No hagas git pull si tienes cambios locales sin guardar**: revisa primero \`git status\`. Los cambios realizados directamente en ~/.config no se guardan en el repositorio; compáralos con los nuevos archivos antes de reinstalar.

No reinstales ni reinicies SDDM en cada actualización. Solo si cambian los archivos del tema del greeter, revisa el diff y ejecuta de nuevo, expresamente, **sudo sh sddm/install-theme.sh NOMBRE**.

## 8. Recuperación desde TTY

Si Qtile falla, cambia a una TTY con **Ctrl+Alt+F3** e inicia sesión. Revisa el error:

~~~bash
qtile check -c "$HOME/.config/qtile/config.py"
journalctl --user -b --no-pager -n 100
~~~

Los respaldos del instalador tienen la forma **~/.config/qtile.backup.FECHA-PID** (y lo mismo para Fish, Alacritty, etc.). Identifica la copia adecuada:

~~~bash
ls -ld "$HOME/.config/qtile.backup."*
~~~

Para recuperar **únicamente Qtile**, sustituye la ruta de respaldo por la que has comprobado:

~~~bash
mv "$HOME/.config/qtile" "$HOME/.config/qtile.failed"
mv "$HOME/.config/qtile.backup.FECHA-PID" "$HOME/.config/qtile"
~~~

Si SDDM se muestra en negro o no permite iniciar sesión, vuelve a una TTY y desactiva únicamente el override del tema sin tocar PAM:

~~~bash
sudo mv /etc/sddm.conf.d/90-operator-hud.conf \
  /etc/sddm.conf.d/90-operator-hud.conf.disabled
~~~

Después reinicia SDDM o el equipo cuando sea seguro hacerlo. Consulta **sddm/README.md** para distinguir un problema QML de un fallo PAM, GPU o de sesión. No borres otros gestores de acceso mientras depuras.

## 9. Referencia de atajos

| Atajo | Acción |
| --- | --- |
| Super+Enter | Alacritty + Fish |
| Super+1…8 / Super+Shift+1…8 | Cambiar de grupo / mover ventana |
| Super+h/j/k/l | Cambiar el foco (Vim) |
| Super+Shift+h/j/k/l | Reordenar |
| Super+Ctrl+h/j/k/l | Redimensionar, según layout |
| Super+Tab | Siguiente layout |
| Super+F | Alternar pantalla completa |
| Super+Shift+Espacio | Alternar flotante |
| Super+tecla grave | Terminal ScratchPad |
| Super+Shift+tecla grave | Panel btop (opcional) |
| Super+P | Menú Operator HUD |
| Super+M / Super+Shift+M | Lanzador / lista de ventanas |
| Super+Shift+T | Selector de temas |
| Super+Shift+V | Selector WireGuard (NetworkManager) |
| Super+Shift+P | Menú de energía y bloqueo |
| Super+E | Thunar |
| Super+S / Super+Shift+S | Captura completa / área |
| Super+W | Cerrar ventana |
| Super+Ctrl+R | Recargar configuración Qtile |
| Super+Ctrl+Q | Cerrar sesión Qtile |

El listado completo y los atajos de aplicaciones adicionales están en **.config/qtile/settings/keys.py** y **groups.py**.

## 10. Arquitectura y mantenimiento

| Directorio | Función |
| --- | --- |
| .config/qtile/ | Ventanas, layouts, barra, atajos, autostart, bloqueo y selector de temas |
| .config/alacritty/ | Terminal TOML y perfiles ANSI |
| .config/fish/ | Prompt, completado y funciones |
| .config/fastfetch/ | Resumen de sistema y perfiles |
| .config/rofi/ | Lanzador y tema del menú |
| .config/dunst/ | Notificaciones |
| .config/picom/ | Composición X11 |
| sddm/operator-hud/ | Greeter Qt6 y perfiles de tres temas |
| sddm/install-theme.sh | Instalador administrativo de greeter |
| scripts/install-dotfiles.sh | Instalador de usuario y respaldos |
| tests/ | Validación estática ejecutable con Python |
| .github/workflows/ | Pruebas automáticas en PR |

El repositorio no versiona temas GTK, asociaciones MIME privadas ni archivos universales generados por Fish. No modifica **~/.bashrc** automáticamente. **SDDM y PAM permanecen separados** de las configuraciones de usuario.

## Documentación oficial

- [ArchWiki: Installation guide](https://wiki.archlinux.org/title/Installation_guide)
- [ArchWiki: Qtile](https://wiki.archlinux.org/title/Qtile)
- [Qtile: documentación](https://docs.qtile.org/en/stable/)
- [ArchWiki: Xinit](https://wiki.archlinux.org/title/Xinit)
- [ArchWiki: SDDM](https://wiki.archlinux.org/title/SDDM)
- [ArchWiki: PAM](https://wiki.archlinux.org/title/PAM)
- [ArchWiki: Polkit](https://wiki.archlinux.org/title/Polkit)
- [ArchWiki: NVIDIA](https://wiki.archlinux.org/title/NVIDIA)
- [ArchWiki: PipeWire](https://wiki.archlinux.org/title/PipeWire)
- [SDDM: temas QML](https://github.com/sddm/sddm/blob/develop/docs/THEMING.md)

**Validación:** los tests automatizados y la revisión estática no sustituyen una prueba real con tu hardware y sesión X11. Antes de considerar seguro el sistema, verifica autenticación, bloqueo, recuperación y suspensión. Este repositorio no incluye un archivo LICENSE.
