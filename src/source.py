import os
import sys
from pprint import pprint

_base_path = sys._MEIPASS if getattr(sys, "frozen", False) else os.path.curdir


def _get_path(*args):
    return os.path.join(_base_path, *args)


src_path = {
    # icon
    "qrcode": _get_path("icon", "qrcode.ico"),
    # pics
    "goto": _get_path("pics", "goto.png"),
    "import": _get_path("pics", "import.png"),
    "screenshot": _get_path("pics", "screenshot.png"),
}


if __name__ == "__main__":
    pprint({path: src_path[path] for path in src_path})
