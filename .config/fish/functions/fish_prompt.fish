function fish_prompt --description "Obsidian: two-line prompt with Git and Python environment"
    set -l last_status $status
    set -g __obsidian_last_status $last_status

    set_color 778895
    printf '╭─ '

    if set -q SSH_CONNECTION
        set_color E7C78F
        printf '%s@%s ' "$USER" (prompt_hostname)
    else if fish_is_root_user
        set_color E78991
        printf 'root '
    end

    set_color --bold 82CDBE
    printf '%s' (prompt_pwd --dir-length=2)
    set_color normal

    set -l git_info (fish_git_prompt ' (%s)')
    if test -n "$git_info"
        set_color A8BED3
        printf '%s' "$git_info"
    end

    if set -q VIRTUAL_ENV
        set_color C3AADF
        printf '  py:%s' (path basename -- "$VIRTUAL_ENV")
    end

    printf '\n'
    set_color 778895
    printf '╰─'
    if test $last_status -eq 0
        set_color 82CDBE
    else
        set_color E78991
    end
    printf '❯ '
    set_color normal
end
