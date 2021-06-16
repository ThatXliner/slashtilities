import logging

from rich.logging import RichHandler

from . import database

__version__ = "0.1.0"
FORMAT = "%(asctime)s %(message)s"
logging.basicConfig(
    level=logging.INFO,
    format=FORMAT,
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)],
)

log = logging.getLogger(__name__)
db = database.Database()
