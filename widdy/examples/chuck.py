import requests
from html.parser import HTMLParser
from widdy import widdy

class Chuck(widdy.App):
    def get_joke(app):
        joke = requests.get('http://api.icndb.com/jokes/random').json()
        return HTMLParser().unescape(joke['value']['joke']).encode('utf-8')

    def next_joke(app):
        app.update_text('Getting new quote...')
        app.draw_screen()
        joke = app.get_joke()
        app.update_text(joke)

    def __init__(app):
        h = widdy.Header("Random Quotes")
        m = widdy.Menu(('R', widdy.GREEN_BOLD, 'new quote'))
        t, app.update_text = widdy.Text('Press (R) to get your first quote...')
        b = widdy.LineBox(t)
        f = widdy.Frame(h,b,m)
        handlers = widdy.Handlers(('R', app.next_joke))
        super().__init__(f, handlers=handlers)

def main(): Chuck().run()

if __name__ == '__main__': main()

