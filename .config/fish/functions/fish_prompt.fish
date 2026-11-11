function fish_prompt --description "Obsidian: two-line prompt with Git and Python environment"
    set -l last_status $status
    set -g __obsidian_last_status $last_status

    set_color $__theme_muted
    printf '╭─ '

    if set -q SSH_CONNECTION
        set_color $__theme_warning
        printf '%s@%s ' "$USER" (prompt_hostname)
    else if fish_is_root_user
        set_color $__theme_alert
        printf 'root '
    end

    set_color --bold $__theme_accent
    printf '%s' (prompt_pwd --dir-length=2)
    set_color normal

    set -l git_info (fish_git_prompt ' (%s)')
    if test -n "$git_info"
        set_color $__theme_secondary
        printf '%s' "$git_info"
    end

    if set -q VIRTUAL_ENV
        set_color $__theme_python
        printf '  py:%s' (path basename -- "$VIRTUAL_ENV")
    end

    printf '\n'
    set_color $__theme_muted
    printf '╰─'
    if test $last_status -eq 0
        set_color $__theme_accent
    else
        set_color $__theme_alert
    end
    printf '❯ '
    set_color normal
end
