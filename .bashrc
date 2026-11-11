# Bash fallback only. Alacritty launches Fish.
[[ $- == *i* ]] || return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

# Subtle Obsidian colors for interactive Bash.
PS1='\[\e[38;2;130;205;190m\]\u@\h \[\e[38;2;201;214;225m\]\w\[\e[0m\] \$ '
