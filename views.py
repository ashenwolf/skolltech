from decorators import render_to, BaseHandler 

class home(BaseHandler):
    @render_to("index.html", 0)
    def get(self):
        return {
        }
