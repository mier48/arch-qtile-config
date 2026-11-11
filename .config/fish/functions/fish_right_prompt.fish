function fish_right_prompt --description "Obsidian: exit code, duration, clock"
    if set -q __obsidian_last_status
        if test $__obsidian_last_status -ne 0
            set_color $__theme_alert
            printf 'exit:%s  ' $__obsidian_last_status
        end
    end

    if set -q CMD_DURATION
        if test $CMD_DURATION -ge 1000
            set_color $__theme_secondary
            printf '%ss  ' (math --scale=1 "$CMD_DURATION / 1000")
        end
    end

    set_color $__theme_muted
    printf '%s' (date '+%H:%M')
    set_color normal
end
