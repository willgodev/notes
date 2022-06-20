"===General==="
"===Numbering==="
" Toggle current line number as well
set number

"===Syntax==="
" Turn on syntax highlightig
syntax on

"===Indentation==="
" Copy indent from the current line when starting new line
set autoindent
" Replace tabs with whitespace characters
set expandtab
" Set tab size
set shiftwidth=4
" A tab character indents to the 4nd column
set tabstop=4

"===Searching==="
" Search highlighting
set hlsearch
" Incremental search
set incsearch
" In order to toggle smartcase
set ignorecase
" If search contains capital letter, case-sensitive search
" If not, case-insensitive search
set smartcase

"===Cursor==="
" Always show cursor position
set ruler
" Highlight current line
set cursorline
" Mouse compatibility
set mouse=a

"===Buffers==="
" Allows faster navigation between buffers
" (Doesn't require save or force quit to switch)
set hidden

"===Navigation==="
" Number of lines to keep on screen when scrolling
set scrolloff=10

"===Misc==="
" Backspace behaviors
set backspace=indent,eol,start
" Map leader to semicolon
let mapleader = ";"
" Show commands
set showcmd
set background=dark

"===Mappings==="
" Alt + j/k to move lines up and down
nnoremap <A-j> :m .+1<CR>==
nnoremap <A-k> :m .-2<CR>==
inoremap <A-j> <Esc>:m .+1<CR>==gi
inoremap <A-k> <Esc>:m .-2<CR>==gi
vnoremap <A-j> :m '>+1<CR>gv=gv
vnoremap <A-k> :m '<-2<CR>gv=gv

imap jk <ESC>
cnoremap jk <ESC>
