# Palette matches ~/.config/qtile/themes/obsidian.json
# Global scope overrides legacy universal colors in fish_variables.
if status is-interactive
    set -g fish_color_normal A9B7C6
    set -g fish_color_command 6A8759
    set -g fish_color_keyword 6A8759
    set -g fish_color_param A9B7C6
    set -g fish_color_option 9876AA
    set -g fish_color_quote FFC66D
    set -g fish_color_comment 808A91
    set -g fish_color_error BC3F3C
    set -g fish_color_end 6A8759
    set -g fish_color_operator 9876AA
    set -g fish_color_escape 9876AA
    set -g fish_color_redirection 6897BB
    set -g fish_color_autosuggestion 68737B
    set -g fish_color_search_match --background=4E5254
    set -g fish_color_selection E8E8E8 --background=4E5254
    set -g fish_color_valid_path --underline
    set -g fish_color_cwd 6A8759
    set -g fish_color_cwd_root BC3F3C
    set -g fish_color_status BC3F3C
    set -g fish_color_host_remote FFC66D

    set -g fish_pager_color_completion A9B7C6
    set -g fish_pager_color_description 808A91
    set -g fish_pager_color_prefix 6A8759 --bold
    set -g fish_pager_color_progress A9B7C6 --background=3C3F41
    set -g fish_pager_color_selected_background --background=4E5254
    set -g fish_pager_color_selected_completion E8E8E8
    set -g fish_pager_color_selected_description A9B7C6
end

# Dynamic prompt palette: Darcula
set -g __theme_muted 808A91
set -g __theme_accent CC7832
set -g __theme_alert BC3F3C
set -g __theme_warning FFC66D
set -g __theme_secondary 9876AA
set -g __theme_python 9876AA
