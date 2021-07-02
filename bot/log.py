import discord, logging, os

logger = logging.getLogger("discord")
logger.setLevel(logging.WARNING)

log_path = os.path.join(os.getcwd(), "gonk.log")
handler = logging.FileHandler(filename=log_path, encoding="utf-8", mode="w")
handler.setFormatter(
    logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
)

logger.addHandler(handler)
