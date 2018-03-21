import requests
from html.parser import HTMLParser
from ohlcwid import ohlcwid

class Chuck(ohlcwid.App):
    def get_joke(app):
        joke = requests.get('http://api.icndb.com/jokes/random').json()
        return HTMLParser().unescape(joke['value']['joke']).encode('utf-8')

    def update_joke(app):
        app.update_text('Getting new quote...')
        app.draw_screen()
        joke = app.get_joke()
        app.update_text(joke)

    def __init__(app):
        h = ohlcwid.Header("Random Quotes")
        m = ohlcwid.Menu(('R', ohlcwid.GREEN_BOLD, 'new quote'))
        t, app.update_text = ohlcwid.Text('Press (R) to get your first quote...')
        b = ohlcwid.LineBox(t)
        f = ohlcwid.Frame(h,b,m)
        handlers = ohlcwid.Handlers(('R', app.update_joke))
        super().__init__(f, handlers=handlers)

def main(): Chuck().run()

if __name__ == '__main__': main()

