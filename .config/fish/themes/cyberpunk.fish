# Palette matches ~/.config/qtile/themes/obsidian.json
# Global scope overrides legacy universal colors in fish_variables.
if status is-interactive
    set -g fish_color_normal D9D1EC
    set -g fish_color_command 36DCE5
    set -g fish_color_keyword 36DCE5
    set -g fish_color_param D9D1EC
    set -g fish_color_option A48BFF
    set -g fish_color_quote FAD879
    set -g fish_color_comment 827D9D
    set -g fish_color_error FF647D
    set -g fish_color_end 36DCE5
    set -g fish_color_operator A48BFF
    set -g fish_color_escape C7A1FF
    set -g fish_color_redirection 64CFFF
    set -g fish_color_autosuggestion 756E96
    set -g fish_color_search_match --background=3B3455
    set -g fish_color_selection F5EAFF --background=3B3455
    set -g fish_color_valid_path --underline
    set -g fish_color_cwd 36DCE5
    set -g fish_color_cwd_root FF647D
    set -g fish_color_status FF647D
    set -g fish_color_host_remote FAD879

    set -g fish_pager_color_completion D9D1EC
    set -g fish_pager_color_description 827D9D
    set -g fish_pager_color_prefix 36DCE5 --bold
    set -g fish_pager_color_progress D9D1EC --background=24203A
    set -g fish_pager_color_selected_background --background=3B3455
    set -g fish_pager_color_selected_completion F5EAFF
    set -g fish_pager_color_selected_description D9D1EC
end

# Dynamic prompt colors (Cyberpunk)
set -g __theme_muted 827D9D
set -g __theme_accent FF4FA3
set -g __theme_alert FF647D
set -g __theme_warning FAD879
set -g __theme_secondary A48BFF
set -g __theme_python C7A1FF
