import subprocess
from pathlib import Path


def test_requirementstxt_is_up_to_date() -> None:
    ...
    #assert (
    #    subprocess.check_output(["poetry", "export", "--without-hashes"]).decode().strip()
    #    == Path("requirements.txt").read_text().strip()
    #)
