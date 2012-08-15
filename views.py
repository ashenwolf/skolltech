from decorators import render_to, BaseHandler 

class home(BaseHandler):
    @render_to("index.html")
    def get(self):
        return {}
