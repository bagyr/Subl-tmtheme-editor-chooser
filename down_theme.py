import sublime
import sublime_plugin
import urllib2
import json
import os


class ThemesApi():

    def __init__(self):
        self.themes = {}
        self.themeNames = []
        self.url = "http://tmtheme-editor.herokuapp.com/gallery.json"

    def loadThemes(self):
        http_file = urllib2.urlopen(self.url)
        result = http_file.read()
        json_themes = json.loads(result)
        for item in json_themes:
            self.themeNames.append(item['name'])
            self.themes[item['name']] = item['url']

    def saveTheme(self, pos):
        themeFile = self.themes[self.themeNames[pos]]

        localFile = os.path.join(sublime.packages_path(), themeFile.split('/')[-1])
        req = urllib2.urlopen(themeFile)
        with open(localFile, 'wb') as fp:
            fp.write(req.read())
        return os.path.join('Packages', themeFile.split('/')[-1])


class DownThemeCommand(sublime_plugin.WindowCommand):

    apiCall = ThemesApi()

    def run(self):
        self.apiCall.loadThemes()
        self.window.show_quick_panel(self.apiCall.themeNames, self.on_quick_done, sublime.MONOSPACE_FONT)

    def on_quick_done(self, pos):
        theme = self.apiCall.saveTheme(pos)
        print theme
        s = sublime.load_settings('Preferences.sublime-settings')
        s.set("color_scheme", theme)
        sublime.set_settings('Preferences.sublime-settings')
