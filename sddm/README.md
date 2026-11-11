# Operator HUD · SDDM Qt6

Tema para el **greeter SDDM Qt 6** independiente del bloqueo de la sesión X11. Paletas: Obsidian, Cyberpunk y Darcula.

## Principios de seguridad

- El tema QML **no autentica credenciales**: utiliza `sddm.login(username, password, sessionIndex)` y deja la verificación en SDDM/PAM.
- Solicita el nombre del usuario en lugar de mostrar una lista de cuentas, reduciendo exposición casual de identidades.
- No existe inicio automático, ni almacenamiento, ni registro de contraseñas.
- Tras un error, vacía el campo de contraseña; no modifica `/etc/pam.d/` ni `/etc/security/`.
- La pantalla SDDM es un **greeter de inicio de sesión**. No sustituye i3lock para proteger una sesión ya abierta.
- La disponibilidad de sesiones procede de `sessionModel`; selecciona explícitamente Qtile X11 cuando sea necesario.

## Instalación controlada

Desde la raíz del repositorio:

```bash
sudo pacman -S --needed sddm qt6-declarative qt6-svg
sudo sh sddm/install-theme.sh cyberpunk
```

Cambia `cyberpunk` por `obsidian` o `darcula` para instalar cualquiera. Cada perfil tiene un `theme.conf` con sección `[General]`, que es la que lee `config` en el QML de SDDM. El instalador crea `/usr/share/sddm/themes/operator-TEMA/` y `/etc/sddm.conf.d/90-operator-hud.conf` (con copia de seguridad cuando existe). **No habilita SDDM, no reinicia la sesión y no cambia PAM.**

No ejecutes el instalador desde una ruta ajena o un repositorio que no hayas revisado; es un script con privilegios de administrador.

## Sincronizar SDDM con Qtile

El tema de SDDM **no se cambia automáticamente** desde `Super+Shift+T`: SDDM es un proceso privilegiado independiente de la sesión del usuario.

Desde la raíz del repositorio puedes instalar explícitamente el tema que has seleccionado en Qtile:

```sh
sudo sh sddm/install-theme.sh --from-qtile
```

Para ver el override que ha creado el instalador:

```sh
sh sddm/install-theme.sh --current
cat /etc/sddm.conf.d/90-operator-hud.conf
cat /usr/share/sddm/themes/operator-cyberpunk/theme.conf
```

Espera `Current=operator-cyberpunk` y una sección `[General]` con `accent=#FF4FA3` cuando Cyberpunk esté seleccionado. El selector no modifica automáticamente SDDM para evitar elevar privilegios desde el escritorio. Si alguna otra configuración define `[Theme] Current`, comprueba su prioridad con `sddm --example-config` y revisa `/etc/sddm.conf` y `/etc/sddm.conf.d/`.

## Prueba sin modificar la sesión

Comprueba si existe el greeter Qt6:

```bash
command -v sddm-greeter-qt6
pacman -Ql sddm | grep '/sddm-greeter'
sddm-greeter-qt6 --help
```

Prueba el tema de forma aislada en una sesión gráfica de prueba (puede requerir Xephyr y los módulos Qt6 correspondientes según versión):

```bash
sddm-greeter-qt6 --test-mode --theme /usr/share/sddm/themes/operator-cyberpunk
```

En Arch Linux, el ejecutable Qt6 se encuentra en `/usr/bin/sddm-greeter-qt6`. En algunas versiones se utiliza `sddm-greeter --test-mode --theme RUTA`. Consulta `sddm-greeter --help` para la sintaxis de tu versión. El modo de prueba no comprueba autenticación real, PAM ni logind.

Solo **después de verificar el tema**, activa SDDM manualmente si no utilizas otro display manager:

```bash
systemctl status display-manager.service
sudo systemctl enable sddm.service
```

**No habilites dos gestores de acceso simultáneamente.** Si ya utilizas GDM/LightDM, desactiva el anterior siguiendo su documentación y conserva una TTY de recuperación. No añadas `DisplayServer=wayland`: el objetivo sigue siendo Qtile X11.

## Recuperación

Desde una TTY (Ctrl+Alt+F3), inicia sesión y revisa:

```bash
systemctl status sddm.service
journalctl -b -u sddm.service --no-pager -n 80
ls -al /etc/sddm.conf.d/
```

Para volver al tema predeterminado, renombra solamente nuestro override:

```bash
sudo mv /etc/sddm.conf.d/90-operator-hud.conf /etc/sddm.conf.d/90-operator-hud.conf.disabled
```

No edites `/etc/pam.d/sddm` para recuperar el tema. Los archivos de copia `*.backup.FECHA` sirven para restaurar la configuración anterior.

## Sincronización de temas

El selector de colores de Qtile se ejecuta como usuario normal y **no modifica** `/usr/share/sddm/themes/` ni `/etc/sddm.conf.d/`. Para cambiar el tema de SDDM vuelve a ejecutar expresamente el instalador con `sudo`. Esto evita otorgar permisos de escritura privilegiados al usuario del escritorio.

## Referencias

- [ArchWiki · SDDM](https://wiki.archlinux.org/title/SDDM)
- [SDDM · Theming](https://github.com/sddm/sddm/blob/develop/docs/THEMING.md)
- [ArchWiki · PAM](https://wiki.archlinux.org/title/PAM)
- [ArchWiki · systemd](https://wiki.archlinux.org/title/Systemd)
