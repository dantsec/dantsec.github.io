---
title: Tmux @ Crash Course
published: 2026-02-02
description: 'Main concepts of Tmux that you need to know.'
image: ''
tags: [Crash-Course, Tools]
category: Tools
draft: false
lang: 'pt-br'
---

# Introduction

- Known as a terminal multiplexer that allows you to craft a single terminal however you need it;
- It is case sensitive, take care;
- The prefix key is `C-b` (`ctrl + b`);
- Fun commands:
	- `C-b + t`: show time in the pane.

# Commands

## Sessions

### Out of Windows / Panes

- `tmux`: start a session (with default name `0`);
- `tmux ls`: list active sessions;
- `tmux new -s [SESSION_NAME] -d` or `tmux new`: create a new session;
	- By default, tmux always waits for you to be disconnected from a session before creating another one, that's why we need the `d` (_detach_) parameter.
- `tmux a -t [SESSION_NAME]`: connect (attach) to a session based on listed sessions;
- `tmux kill-session -t [SESSION_NAME]`: kill a session based on it's name;
	- If you use `-a` in the end of the command, it will delete all sessions except the specifiend in `-t` argument;
- `tmux kill-server`: kill all tmux proccesses.

### Inside of Windows / Panes

- `C-b + s + [ARROW_KEYS|SESSION_ID]`: inside a active window, change current session;
- `C-b + $`: rename current session;
- `C-b + [(|)]`: go to previous / next session;
- `C-b + :`: it's like a tmux prompt inside pane (you can execute ls, kill and other tmux commands);
	- `a -c /path/to/new/starting/directory`: update starting / base directory;
	- `swap-pane -s [SOURCE_PANE] -t [CURRENT_PANE]`: swap position of _CURRENT_PANE_ to _SOURCE_PANE_;
	- `join-pane -s [SOURCE_PANE] [-v|-h]`: concatenate _SOURCE_PANE_ (number or name) to current pane, `-v` to concatenate vertically and `-h` to concatenate horizontally; same logic is applied to use with `-t` instead of `-s` (here we join our current pane to _DESTINATION_PANE_),

## Panes

> Press `C-b`, drop and then press wanted key.

- `C-b + %`: split the screen into two horizontal panes;
- `C-b + "`: split the screen into upper and lower panes;
- `C-b + [ARROW_KEYS]`:
	- **Dropping C-b**: moves between panes;
	- **Holding C-b**: resizes the active pane;
- `C-b + d`: detaches from a session;
- `C-d` / `C-b + x` / `exit`: kill the pane;
- `C-b + [{|}]`: move pane to left / right;
- `C-b + spacebar`: swap position and size of all panes;
	- `C-b + q`: show each pane id and size (useful to make swaps).

## Window

> The hierarchy is: session > windows > panes

- `C-b + c`: create a new window;
- `C-b + ,`: rename window;
- `C-b + .`: change window number;
- `C-b + [WINDOW_NUMBER]`: select window by number;
- `C-b + '`: select window by name;
- `C-b + !`: transform current window into a pane;
- `C-b + w + [ARROW_KEYS|SESSION_ID]`: list windows to give a view to cycle trough them (tree view);
- `C-b + &`: kill window;
- `C-b + [p|n]`: move to previous / next window.

## Copy Mode

> Similar to _less_, Unix utilitary. Scroll up / dodwn the page.

- `C-b + [`: enter in _copy mode_, use `q` to quit;
- `[ARROW_KEYS]`: go up / down through the pane;
- `g + [LINE_NUMBER]`: go to provided line;
- `C-r` / `C-s`: search **up** / **down** for term or string;
	- After typing term, press `C-r` or `C-s` to continue viewing the terms found;
	- Type `esc` or `q` to clear selection / exit.
- **Selecting text and copy / paste it**:
	- `C-b [` to enter in copy mode;
	- `C-spacebar + [ARROW_KEYS]` to select text;
	- `alt w`: to move highlighted text to the tmux clipboard;
	- `C-b ]`: paste.
- `C-b + #`: list all buffers.

# Configuration

- To show all current configurations, type `tmux show -g`;
- The configuration file is `~/.tmux.conf` (there isn't default config file);
	- Here you can set you own binds.
- You can find examples at `/usr/share/doc/tmux/examples/`.
