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
sudo sh sddm/install-theme.sh obsidian
```

Cambia `obsidian` por `cyberpunk` o `darcula` para instalar cualquiera. El instalador crea `/usr/share/sddm/themes/operator-TEMA/` y `/etc/sddm.conf.d/90-operator-hud.conf` (con copia de seguridad cuando existe). **No habilita SDDM, no reinicia la sesión y no cambia PAM.**

No ejecutes el instalador desde una ruta ajena o un repositorio que no hayas revisado; es un script con privilegios de administrador.

## Prueba sin modificar la sesión

Comprueba si existe el greeter Qt6:

```bash
ls /usr/lib/sddm/sddm-greeter* 2>/dev/null
```

Prueba el tema de forma aislada en una sesión gráfica de prueba (puede requerir Xephyr y los módulos Qt6 correspondientes según versión):

```bash
sddm-greeter-qt6 --test --theme /usr/share/sddm/themes/operator-obsidian
```

Si la orden no está en tu PATH, utiliza la ruta absoluta del binario correspondiente (habitualmente bajo `/usr/lib/sddm/`). En algunas versiones se utiliza `sddm-greeter --test --theme RUTA`. Consulta `sddm-greeter --help` para la sintaxis de tu versión. El modo de prueba no comprueba autenticación real, PAM ni logind.

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
