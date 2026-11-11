# Palette matches ~/.config/qtile/themes/obsidian.json
# Global scope overrides legacy universal colors in fish_variables.
if status is-interactive
    set -g fish_color_normal C9D6E1
    set -g fish_color_command 82CDBE
    set -g fish_color_keyword 82CDBE
    set -g fish_color_param C9D6E1
    set -g fish_color_option A8BED3
    set -g fish_color_quote E7C78F
    set -g fish_color_comment 778895
    set -g fish_color_error E78991
    set -g fish_color_end 82CDBE
    set -g fish_color_operator A8BED3
    set -g fish_color_escape C3AADF
    set -g fish_color_redirection 8FAFD1
    set -g fish_color_autosuggestion 657989
    set -g fish_color_search_match --background=35434F
    set -g fish_color_selection EDF3F8 --background=35434F
    set -g fish_color_valid_path --underline
    set -g fish_color_cwd 82CDBE
    set -g fish_color_cwd_root E78991
    set -g fish_color_status E78991
    set -g fish_color_host_remote E7C78F

    set -g fish_pager_color_completion C9D6E1
    set -g fish_pager_color_description 778895
    set -g fish_pager_color_prefix 82CDBE --bold
    set -g fish_pager_color_progress C9D6E1 --background=233341
    set -g fish_pager_color_selected_background --background=35434F
    set -g fish_pager_color_selected_completion EDF3F8
    set -g fish_pager_color_selected_description C9D6E1
end

# Shared prompt colors (Obsidian)
set -g __theme_muted 778895
set -g __theme_accent 82CDBE
set -g __theme_alert E78991
set -g __theme_warning E7C78F
set -g __theme_secondary A8BED3
set -g __theme_python C3AADF
