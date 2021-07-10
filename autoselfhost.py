import subprocess
import shutil
import sys
import ensurepip
import platform
from typing import NoReturn
import re
from pathlib import Path

MINIMUM_PY = (3, 7)
git = shutil.which("git")
poetry = shutil.which("poetry")
psql = shutil.which("psql")
python3x = (
    shutil.which("python3.7") or shutil.which("python3.8") or shutil.which("python3.9")
)
python = shutil.which("python3") or shutil.which("python")
THIS = sys.executable
PIP_PY_VER_RE = re.compile(r"\(python (\d+)\.(\d+)\)")


def error(msg: str) -> NoReturn:
    if platform.system() == "Windows":
        print(f"Error: {msg}")
    else:
        print(f"\033[31mError: {msg}\033[0m")
    sys.exit(1)


def info(msg: str) -> None:
    if platform.system() == "Windows":
        print(f"[+] {msg}")
    else:
        print(f"\033[33m[+]\033[37m {msg}\033[0m")


def get_pip() -> str:
    pip = shutil.which("pip") or shutil.which("pip3")
    if pip is not None:
        pip_ver = PIP_PY_VER_RE.search(subprocess.check_output([pip, "-V"]).decode())
        if (pip_ver[1], pip_ver[2]) >= 3.7:
            return pip
    ensurepip.bootstrap(upgrade=True)
    return f"{THIS} -m pip"


not_found = {}
found = {}
print(" Checking requirements ".center(shutil.get_terminal_size().columns, "="))
print()
print(" - git", end="...", flush=True)
if git is not None:
    print(f"found ({git})")
    found["git"] = git
else:
    print("not found")
    not_found["Git"] = "Please install Git from https://git-scm.com/downloads"

print(" - Python 3.7+", end="...", flush=True)
if sys.version_info[0:2] >= MINIMUM_PY:
    print("found (the Python used to run this script)")
    found["python"] = THIS
elif python3x is not None:
    print(f"found ({python3x})")
    found["python"] = python3x
elif (
    python is not None
    and [
        int(x) for x in subprocess.check_output([python, "-V"]).decode()[7:].split(".")
    ][0:2]
    >= MINIMUM_PY
):
    print(f"found ({python})")
    found["python"] = python
else:
    print("not found")
    not_found[
        "Python"
    ] = "Please install the latest version of Python from https://www.python.org/downloads/"

print(" - Poetry (optional)", end="...", flush=True)
if poetry is not None:
    print(f"found ({poetry})")
    found["poetry"] = poetry
else:
    print("not found, that's ok!")

print(" - PostgreSQL", end="...", flush=True)
if psql is not None:
    print(f"found ({psql})")
    found["psql"] = psql
else:
    print("not found, that's ok!")
    found["psql"] = None

if not_found:
    error(
        "Some requirements where not found\n"
        + "\n".join((f"{thing}: {how}" for thing, how in not_found.items()))
    )
print()
print("=" * shutil.get_terminal_size().columns)

print("Resolving pip", end="...", flush=True)
USE_PIP = False
if found.get("poetry"):
    print("Nevermind, we have poetry")
else:
    found["pip"] = get_pip()
    print(found["pip"])
    USE_PIP = True

info("Cloning slashtilities")
subprocess.run(
    [found["git"], "clone", "https://github.com/ThatXliner/slashtilities.git"],
    check=True,
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
)
SLASH_PATH = str(Path(".").resolve().joinpath("slashtilities"))
if USE_PIP:
    info("Creating virtual environment")
    subprocess.run(
        [found["python"], "-m", "venv", ".venv"],
        check=True,
        cwd=SLASH_PATH,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
    info("Setting up virtual environment")
    subprocess.run(
        f"source .venv/bin/activate && {found['pip']} install -r requirements.txt",
        shell=True,
        check=True,
        cwd=SLASH_PATH,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )
else:
    info("Running `poetry install`")
    subprocess.run(
        [found["poetry"], "install"],
        check=True,
        cwd=SLASH_PATH,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT,
    )

print("=" * shutil.get_terminal_size().columns)
print("All set!\n")
if found["psql"] is None:
    print("WARNING: PostgreSQL didn't seemed to be installed")
    print("Slashtilities can still function without PostgreSQL but")
    print("settings and configuration will not be enabled")
print("To run the bot, go to the slashtilities directory and run")
print()
if USE_PIP:
    print("    source .venv/bin/activate")
    print(
        f"{'    NO_DB=1 ' if found['psql'] is None else '    '}DISCORD_TOKEN=<your discord token here> python3 -m slashtilities"
    )

else:
    print(
        f"{'    NO_DB=1 ' if found['psql'] is None else '    '}DISCORD_TOKEN=<your discord token here> poetry run python -m slashtilities"
    )

print()
print("Where `<your discord token here>` is your Discord bot's token")
