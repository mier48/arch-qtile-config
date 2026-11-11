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
        abbr --add sys 'fastfetch'
    end

    if type -q zoxide
        zoxide init fish | source
    end
end
