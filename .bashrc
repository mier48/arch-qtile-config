# Minimal Bash fallback — Alacritty uses Fish by default.
[[ $- == *i* ]] || return

alias ls='ls --color=auto'
alias grep='grep --color=auto'

# Pick the same accent as Qtile, once per interactive Bash session.
__qtile_theme=obsidian
if command -v python >/dev/null 2>&1; then
    __qtile_theme=$(python -c 'import json,os,pathlib; p=pathlib.Path(os.path.expanduser("~/.config/qtile/config.json")); print(json.loads(p.read_text()).get("theme","obsidian"))' 2>/dev/null) || __qtile_theme=obsidian
fi
case "$__qtile_theme" in
    cyberpunk) __prompt_accent='255;79;163'; __prompt_text='217;209;236' ;;
    darcula) __prompt_accent='204;120;50'; __prompt_text='169;183;198' ;;
    *) __prompt_accent='130;205;190'; __prompt_text='201;214;225' ;;
esac
printf -v PS1 '\\[\\e[38;2;%sm\\]\\u@\\h \\[\\e[38;2;%sm\\]\\w\\[\\e[0m\\] \\$ ' "$__prompt_accent" "$__prompt_text"
unset __qtile_theme __prompt_accent __prompt_text
