from flask import request


def get_page(arg_name: str = "page") -> int:
    try:
        return int(request.args.get(arg_name, "1"))
    except ValueError:
        return 1
