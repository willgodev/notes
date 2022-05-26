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

call plug#begin('~/.vim/plugged')
    Plug 'neovim/nvim-lspconfig'
    Plug 'Shougo/deoplete.nvim', { 'do': ':UpdateRemotePlugins' }
    Plug 'tbodt/deoplete-tabnine', { 'do': './install.sh' }

    Plug 'vim-airline/vim-airline'
    Plug 'vim-airline/vim-airline-themes'

    Plug 'jiangmiao/auto-pairs'
    Plug 'scrooloose/nerdcommenter'

    Plug 'scrooloose/nerdtree'

    Plug 'neoclide/coc.nvim', { 'branch': 'release' }

    Plug 'sheerun/vim-polyglot'
call plug#end()
let g:deoplete#enable_at_startup = 1
let g:airline_theme = 'raven'

let NERDTreeShowHidden=1

nnoremap <silent> <C-k><C-B> :NERDTreeToggle<CR>

inoremap <silent><expr><tab> pumvisible() ? "\<c-n>" : "\<tab>"
inoremap <silent><expr><s-tab> pumvisible() ? "\<c-p>" : "\<s-tab>"

autocmd InsertLeave,CompleteDone * if pumvisible() == 0 | pclose | endif
