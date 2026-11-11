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

        # Show system summary by default in interactive local shells.
        # Disable explicitly: set -U FASTFETCH_AUTOSTART 0
        # Never run in SSH or nested Fish processes.
        if not set -q SSH_CONNECTION; and not set -q SSH_TTY
            if not set -q FASTFETCH_SHOWN
                if not set -q FASTFETCH_AUTOSTART; or test "$FASTFETCH_AUTOSTART" != 0
                    set -gx FASTFETCH_SHOWN 1
                    command fastfetch
                end
            end
        end
    end

    if type -q zoxide
        zoxide init fish | source
    end
end
