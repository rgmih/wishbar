from pyramid.config import Configurator
from wishbar.server import create_app
import threading
from wishbar.notify import run_bot


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    #t = threading.Thread(target=run_bot)
    #t.daemon = True
    #t.start()
    return create_app()
