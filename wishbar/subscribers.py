from pyramid.renderers import get_renderer
from pyramid.events import BeforeRender, subscriber

@subscriber(BeforeRender)
def add_base_template(event):
    base = get_renderer('pt/base.pt').implementation()
    event.update({'base': base})