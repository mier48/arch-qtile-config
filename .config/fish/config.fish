# Fish Obsidian — interactive features only.
if status is-interactive
    set -g fish_greeting

    # Fast native Git prompt. Do not scan untracked files in huge repos.
    set -g __fish_git_prompt_showdirtystate 1
    set -g __fish_git_prompt_showuntrackedfiles 0
    set -g __fish_git_prompt_showupstream none

    # Abbreviations expand visibly before execution; no shell aliases.
    abbr --add gs 'git status -sb'
    abbr --add ga 'git add'
    abbr --add gc 'git commit'
    abbr --add gd 'git diff'
    abbr --add gl 'git log --oneline --decorate -12'

    if type -q eza
        abbr --add ll 'eza -lah --git --icons=auto --group-directories-first'
    else
        abbr --add ll 'ls -lah'
    end

    if type -q fastfetch
        # System overview: uses ~/.config/fastfetch/config.jsonc by default.
        abbr --add sys 'fastfetch'

        # Explicit opt-in: set -U OBSIDIAN_FASTFETCH_AUTOSTART 1
        # Do not run in SSH or repeat in nested Fish shells.
        if set -q OBSIDIAN_FASTFETCH_AUTOSTART
            if test "$OBSIDIAN_FASTFETCH_AUTOSTART" = 1
                if not set -q SSH_CONNECTION; and not set -q OBSIDIAN_FASTFETCH_SHOWN
                    set -gx OBSIDIAN_FASTFETCH_SHOWN 1
                    command fastfetch
                end
            end
        end
    end

    if type -q zoxide
        zoxide init fish | source
    end
end
