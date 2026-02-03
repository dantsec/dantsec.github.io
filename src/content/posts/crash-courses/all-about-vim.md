---
title: Vim @ Crash Course
published: 2026-02-02
description: 'Main concepts of Vim that you need to know.'
image: ''
tags: [Crash-Course, Tools]
category: Tools
draft: false
lang: 'pt-br'
---

# Introduction

## Getting Help

- To access **Command Mode** type `esc + :`;
- You should use `[h | help] (manual_name)` to get some infos;
- Or just use `F1` or `HELP` key;
- Finally, you can use `esc + : + : [CTRL-D]` to get auto complete of commands.

## What is Vim?

- Vim is a text editor particulary suited for software developers /  programmers;
- **Vim** is _vi improved_, as Vim originated from the famous _vi_ text editor;
- To learn more about vim, you can type `vimtutor` in you shell;
- Some features:
	- Undo;
	- Search and replace;
	- Syntax highlighting;
	- Folding;
	- Extensibility through plugins;
	- ...

## .VIMRC

- This file contains your vim editor configs.

```vim
" Open .vimrc file
:e ~/.vimrc
" Copy template file
:r $VIMRUNTIME/vimrc_example.vim
" Save
:w
" Open vimrc manual
:help vimrc-intro
```

# Navigation

- Vim uses `k (up), j (down), h (left), l (right)` keys for basic document navigation instead of the arrow keys.

## Screen or File

### Screen Position

- `zt`: move the screen to the top of the window;
- `zz`: move the screen to the middle of the window;
- `zb`: move the screen to the bottom of the window.

### Cursor Position

- `H`: move the cursor to the highest line on the screen;
- `M`: move the cursor to the middle line on the screen;
- `L`: move the cursor to the lowest line on the screen;
- `gg`: move the cursor to the begin of file;
- `(line_number) + G`: move the cursor to the selected line or end of file;
- _\`\`_: return to the previous place;
- `''`: return to previous line.

## Words or Content

### Navigation into the Line

- `^`: move to first char in begin line;
- `0`: move to begin of line;
- `$`: move to end line.

### Navigation between Words

> Just remember: You can use numbers to define repetitions. For example, you want to jump word and you use _w_ you can do _2w_ to jump to the second occurrence found.

- `b`: move to begin with the previous word;
- `e`: move to end of current word;
- `w`: move to begin with next word;
- `ge`: move to end of the previous word;

### Jumping over Words

- `fc` or `;`: jump to next char found;
- `Fc` or `,`: jump to previous char found;
- `tc`: jump to next char found (go to previous char);
- `Tc`: jump to previous found (go to next char);
- `*`: jump to next word found;
- `#`: jump to the previous word found.

# Vim Modes

- Vim is a _modal editor_. This means that vim has different modes that can be used to interact with it;
- You can identify which is current type looking at bottom left (when you don't see anything it means you are in normal / command mode);
- There are three modes:
	- **Normal Mode** / **Command Mode** (`esc`): here is where you can do things like _copy_, _paste_, _find_ or _replace_, and execute commands;
	- **Visual Mode** (`v` or `V`): here is where you can select text;
	- **Insert Mode** (`i`): here is where you can write / edit your text.

## Normal Mode

> `()` is optional and `[]` are two or more commands that can be joined.

> You can use `!` to force your action.

- `esc + : + [h | help] + (navigation)`: drop vim helper;
- `esc + : + w + (filename)`: save;
- `esc + : + q`: quit;
- `esc + : + w + q`: save and quit;
- `esc + : + d + (number_of_lines) + d`: remove line under the cursor;
- `esc + : + ! + (shell_command)`: execute external command;
- `esc + : + r + [filename]`: merge two files;
- `esc + : + e + [filename]`: rename file.

## Visual Mode

- `v`: switches to visual mode starting from the character under the cursor;
- `V`: switches to visual mode allowing selection of entire lines, starting with the current line;
- `ctrl + v`: switches to visual mode allowing selection of vertical blocks.

## Insert Mode

- `i`: switches to insert mode and allows to edit text right before the current cursor position;
- `I`: switches to insert mode and places the cursor at the beginning of the line;
- `a`: switches to insert mode and allows to edit text right after the current cursor position;
- `A`: switches to insert mode and places the cursor at the end of the line;
- `o`: switches to insert mode adding a line below the current one;
- `O`: switches to insert mode adding a line above the current one.

# Basic Edition Operations

## Undo & Redo

- `u`: undo the last commands;
- `U`: fix a whole line;
- `ctrl + r`: redo commands (undo the "undos").

## Copy

- First, enter in **visual mode**, and then, try that commands:
	- `y + space`: yank char under the cursor;
	- `yy`: yank the line under the cursor;
	- `(number_of_lines) + yy`: yank the line(s) under the cursor;
	- `yw`: yank word;
	- `y$`: yank to end of line.

## Paste

- `p`: paste after the cursor;
- `P`: paste before the cursor.

## Cut

> You can change _d_ by _c_, the difference is that _c_ cut and change the mode for the insert.

- `d + (number_of_lines) + d`: delete the line under the cursor and copy it;
- `d + (number_of_words) + w`: delete the word and copy it;
- `c$`: delete to end of line;
- `x`: delete current char and copy it;
- `X`: delete previous char and copy it;
- `D`: delete to end of line;
- `ce`: delete to end of word;
- `cc`: remove entire line.

## Delete

- `s`: delete char under the cursor and copy it;
- `S`: delete line under the cursor and copy it.

## Replace

- `r + [letter]`: replace current char by other letter;
- `R`: replace "mode"

## Searching

- `/ + [word]`: search for a word;
- `? + [word]`: search for a word in the backward direction;
- `n`: search for the same phrase again;
- `N`: search for the same phrase again in the opposite direction;
- `ctrl + o`: go back to where you came from;
- `ctrl + i`: goes forward.

## Matching

- Place the cursor on any `(`, `[` or `{` and then type `%`. It finds the matched closer char.

## Substitution

- Go to wanted line and type `:s/old/new/g` to substitute _new_ for _old_.
	- `:#,#s/old/new/g`: where _#,#_ are the line numbers of the range of lines where the substitution is to be done;
	- `:%s/old/new/g`: to change every occurrence in the whole file;
     `:%s/old/new/gc`: to find every occurrence in the whole file, with a prompt whether to substitute or not.
