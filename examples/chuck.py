import requests
from html.parser import HTMLParser
from ccwid import ccwid

class Chuck(ccwid.App):
    def get_joke(app):
        joke = requests.get('http://api.icndb.com/jokes/random').json()
        return HTMLParser().unescape(joke['value']['joke']).encode('utf-8')

    def update_joke(app):
        app.update_text('Getting new quote...')
        app.draw_screen()
        joke = app.get_joke()
        app.update_text(joke)

    def __init__(app):
        h = ccwid.Header("Random Quotes")
        m = ccwid.Menu(('R', ccwid.GREEN_BOLD, 'new quote'))
        t, app.update_text = ccwid.Text('Press (R) to get your first quote...')
        b = ccwid.LineBox(t)
        f = ccwid.Frame(h,b,m)
        handlers = ccwid.Handlers(('R', app.update_joke))
        super().__init__(f, handlers=handlers)

def main(): Chuck().run()

if __name__ == '__main__': main()

