# Intro

A TUI todo-list App using with waybar

# Usage

## CLI

```sh
# list all items in db.json
python main.py ls

# add new item (--ddl)
python main.py add --ddl 2026-5-20

# remove by id
python main.py rm $id
# remove by index
python main.py rm $id --index

# set status(done|undone|reminder|toggle)
python main.py set $status

# clear
python main.py clear
```

# TUI
