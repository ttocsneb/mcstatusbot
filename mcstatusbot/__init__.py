import logging
from contextlib import contextmanager
import signal

from . import logger
from .config import config
from . import bot

_logger = logging.getLogger(__name__)


@contextmanager
def sigint_shutdown():

    original_sigint_handler = signal.getsignal(signal.SIGINT)

    def on_shutdown_req():
        _logger.info("Shutting down Bot..")
        bot.bot.close()
        raise SystemExit

    signal.signal(signal.SIGINT, lambda sig, frame: on_shutdown_req())

    try:
        _logger.info("Press Ctrl-C to shutdown the bot")
        yield
    except Exception:
        raise
    finally:
        signal.signal(signal.SIGINT, original_sigint_handler)


def serve(test=False, debug=False):
    if debug:
        logger.setLogLevel(logging.DEBUG)
        _logger.debug("starting bot in debug mode")

    if not test:
        _logger.info("Starting Bot..")
        with sigint_shutdown():
            bot.bot.run(config.token)
