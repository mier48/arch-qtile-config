# Fish + Alacritty · Obsidian

Rediseño de terminal para Arch Linux + Qtile (X11).

## Fish
- Prompt nativo de dos líneas: ruta acortada, rama Git, Python virtualenv y estado.
- Right prompt: código de salida, tiempo de ejecución (>1 s) y reloj.
- Colores de autocompletado y pager de acuerdo con Qtile.
- Abreviaturas Git (gs, ga, gc, gd, gl), ll (con eza si está instalado) y sys (si existe fastfetch).
- zoxide opcional, cargado solo cuando está instalado.
- No se ejecuta neofetch/fastfetch en cada sesión.
- fish_variables no se toca: lo gestiona Fish. Los colores globales del tema sustituyen a sus colores universales heredados durante la sesión interactiva.

## Alacritty
- Configuración TOML (Alacritty >= 0.13), con colores en themes/obsidian.toml.
- JetBrainsMono Nerd Font 12.5 pt, padding de 14x12 px, opacidad 0.97.
- Sin decoraciones de ventana (Qtile gestiona el foco y los bordes).
- Arranca /usr/bin/fish sin cambiar el login shell del sistema.
- OSC 52 deshabilitado; puede reactivarse manualmente para workflows de copiado remoto.
- Se eliminan alacritty.yml y config.yaml (obsoletos en Alacritty moderno). Los temas YAML históricos permanecen como referencia.

## Instalación
Desde la raíz del repositorio y en la rama de esta propuesta:

    sudo pacman -S --needed fish alacritty ttf-jetbrains-mono-nerd git
    cp -a ~/.config/fish ~/.config/fish.backup.$(date +%Y%m%d-%H%M%S)
    cp -a ~/.config/alacritty ~/.config/alacritty.backup.$(date +%Y%m%d-%H%M%S)
    mkdir -p ~/.config/fish/functions ~/.config/fish/conf.d ~/.config/alacritty/themes
    cp .config/fish/config.fish ~/.config/fish/config.fish
    cp .config/fish/functions/fish_*.fish ~/.config/fish/functions/
    cp .config/fish/conf.d/obsidian.fish ~/.config/fish/conf.d/
    cp .config/alacritty/alacritty.toml ~/.config/alacritty/alacritty.toml
    cp .config/alacritty/themes/obsidian.toml ~/.config/alacritty/themes/

## Validación
    find ~/.config/fish -name '*.fish' -print0 | xargs -0 -n1 fish -n
    alacritty --config-file ~/.config/alacritty/alacritty.toml

Si una terminal anterior usa YAML, arranca una sesión nueva de Alacritty moderno.
El archivo TOML nuevo tiene prioridad sobre antiguos archivos YAML.

## Opcionales
    sudo pacman -S --needed fastfetch zoxide eza

Nota: no se cambia el shell predeterminado del usuario mediante chsh.
