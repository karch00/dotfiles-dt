# Exports
export PATH=$HOME/bin:$HOME/.local/bin:/usr/local/bin:$PATH
export PATH="$PATH:$HOME/.cargo/bin"
export PATH="$PATH:$HOME/.local/bin"
export PATH=$PATH:/home/karch/.spicetify

source ~/.zplug/init.zsh

HISTFILE=$HOME/.zsh_history
HISTSIZE=10000
SAVEHIST=10000

ZSH_THEME="bobbyrussell"


# Zplug Plugins
zplug "junegunn/fzf"
zplug "zsh-users/zsh-autosuggestions"
zplug "Aloxaf/fzf-tab"
zplug "plugins/git", from:oh-my-zsh


# Install and load plugins
if ! zplug check --verbose; then
    printf "Install? [y/N]: "
      if read -q; then
        echo; zplug install
    fi
fi


# Colorizer
ZSH_COLORIZE_TOOL=pygmentize


# FZF config
autoload -Uz compinit bashcompinit; compinit; bashcompinit

export FZF_DEFAULT_OPTS="--height 40% --layout=reverse --border --preview-window=wrap"
export FZF_COMPLETION_TRIGGER='**'
export FZF_TMUX_OPTS="-p80%,60%"

zstyle ":autocomplete:*" widget-style menu-complete
zstyle ":autocomplete:*" fzf-completion yes
zstyle ":fzf-tab:*" fzf-command ftb-tmux-popup
zstyle ":fzf-tab:*" fzf-flags "--pointer=▶" "--height=15" "--layout=reverse" "--border=rounded" "--scroll-off=0" "--ansi" "--color=border:0,pointer:7,bg+:0,fg+:8,hl:8,hl+:8,info:8,prompt:8"


# Keymaps
bindkey "^I" complete-word
bindkey "^[[Z" autosuggest-accept

bindkey "^[[1;5C" forward-word      
bindkey "^[[1;5D" backward-word     

bindkey "^[[H" beginning-of-line    
bindkey "^[[F" end-of-line          


# Starship
eval "$(starship init zsh)"


# Aliases
alias astroterm="astroterm --color --constellations --speed 6000 --fps 64 --city paris -t 10"
alias ls="eza -l --icons=always -M -h --git --git-repos -@ --color=never"


# Load zplug
zplug load

