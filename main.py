import json
from datetime import datetime
import argparse

DB = "db.json"


def clear():
    re_upload([])
    print("all cleared\n")


def re_upload(data):
    with open(DB, "w") as f:
        json.dump(data, f, indent=2)


def load():
    with open(DB, "r") as f:
        return json.load(f)


def add(content, ddl=""):
    data = load()
    for item in data:
        if item["content"] == content:
            print("duplicated item\n")
            return
    new_id = max([item["id"] for item in data], default=0) + 1
    data.append({"id": new_id, "status": -1, "content": content, "deadline": ddl})
    re_upload(data)
    print(content, " added\n")


def get_by_id(id):
    for item in load():
        if item["id"] == id:
            return item["content"]
    return None


def remove(id):
    data = load()
    removed_id = get_by_id(id)
    data = [item for item in data if item["id"] != id]
    re_upload(data)
    print(removed_id, " removed\n")


def set_status(id, status):
    data = load()
    for item in data:
        if item["id"] == id:
            if status == "done":
                item["status"] = 1
                print(item["content"], "done")
            elif status == "undone":
                item["status"] = -1
                print(item["content"], "undone")
            elif status == "reminder":
                item["status"] = 0
                print(item["content"], "is a reminder")
    re_upload(data)


def show():
    data = load()
    for item in data:
        if item["status"] == 1:
            status = "✅"
        elif item["status"] == -1:
            status = "❌"
        else:
            status = "⏰"
        deadline = item["deadline"] or "-"
        print(f"{item['id']: <5} {item['content']: <20} {deadline:<20} {status:<5}")


def args_parse():
    parser = argparse.ArgumentParser(prog="tuido")
    sub = parser.add_subparsers(dest="cmd")

    add_parser = sub.add_parser("add")
    add_parser.add_argument("content")
    add_parser.add_argument("--ddl")

    rm_parser = sub.add_parser("rm")
    rm_parser.add_argument("id", type=int)

    set_parser = sub.add_parser("set")
    set_parser.add_argument("id", type=int)
    set_parser.add_argument("status", choices=["done", "undone", "reminder"])

    sub.add_parser("ls")
    sub.add_parser("clear")

    return parser.parse_args()


if __name__ == "__main__":

    args = args_parse()
    cmd = args.cmd

    if cmd == "add":
        ddl = args.ddl
        if ddl:
            ddl = datetime.strptime(args.ddl, "%Y-%m-%d").strftime("%Y-%m-%d")
        add(args.content, ddl)
    elif cmd == "ls":
        show()
    elif cmd == "rm":
        remove(args.id)
    elif cmd == "set":
        set_status(args.id, args.status)
    elif cmd == "clear":
        clear()
