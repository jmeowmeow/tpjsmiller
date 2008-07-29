import os
import time
import wsgiref.handlers

import names

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    """Processes name generator requests and loads the web template."""
    def p(self, str):
      self.response.out.write(str)

    def getFromRequest(self):
        randomseed = self.request.get("randomseed", default_value=None)

        if (randomseed):
            seed = hash(time.time())
        else:
            seed = self.request.get("seed", default_value=hash(time.time()))
            try:
                intseed = int(seed)
                seed = intseed
            except ValueError: 
                seed = self.request.get("seed", default_value=hash(time.time()))
                pass

        selected = self.request.get("source", default_value="starwars.txt")
        return (seed, selected)

    def get(self):
        (seed, selected) = self.getFromRequest()
        try:
            generatedNames = names.genFromFile(selected, seed)
        except:
            self.response.out.write("<p><em>File not found:</em> "+ selected)
            self.response.out.write("</p><p><a href=\"" + self.request.path + "\">Reload form</a></p>")
            return
        sources = [ 'alphalyrae.txt', 'constellations.txt', 
                    'persian.txt', 'greek.txt', 'middle-earth.txt', 
                    'starwars.txt', 'ellie-anne-kate.txt','gems.txt',
                    'western.txt' ]
        unselected_sources = [ x for x in sources if x != selected ]
        template_values = {
          'seed'     : seed,
          'names'    : generatedNames,
          'sources'  : unselected_sources, 
          'selected' : selected,
          'randomseed' : self.request.get("randomseed", default_value=None,),
          'sourcefile' : self.readContentsOf(selected),
          }
        path = os.path.join(os.path.dirname(__file__), 'index.django')
        self.p(template.render(path, template_values))

    def readContentsOf(self, selected):
        try:
            path = os.path.join(os.path.dirname(__file__), selected)
            f = open(path, 'r')
            return f.read()
        except IOError:
            return ""

def main():
    application = webapp.WSGIApplication(
                                       [('/', MainPage)],
                                       debug=True)
    wsgiref.handlers.CGIHandler().run(application)

if __name__ == "__main__":
  main()
