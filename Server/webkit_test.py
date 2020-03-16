import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2
from gi.repository import GObject
import webkit

window = Gtk.Window()
browser = WebKit2.WebView()
browser.load_uri("https://www.google.com")
window.add(browser)
window.show_all()
Gtk.main()
