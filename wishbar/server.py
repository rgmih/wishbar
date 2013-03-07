from wsgiref.simple_server import make_server

from pyramid.config import Configurator
# from sqlalchemy.orm.exc import NoResultFound
import os
from notify import run_bot
import threading

SETTINGS = {
    'pyramid.reload_templates': 'true'
}

def create_app():
    config = Configurator(settings=SETTINGS)

    path = os.path.abspath(__file__)
    root = path[:path.rindex("/")]
    
    config.add_static_view("css", "{0}/css".format(root))
    config.add_static_view("js", "{0}/js".format(root))
    config.add_static_view("img", "{0}/img".format(root))
    config.add_route("index_route","/")
    config.add_route("logout_route","/logout/")
    config.add_route("login_route","/login/")
    config.add_route("confirm_route","/confirm/{order}")
    config.scan()
    
    app = config.make_wsgi_app()
    return app

if __name__ == '__main__':
    t = threading.Thread(target=run_bot)
    t.daemon = True
    t.start()
     
    app = create_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
    