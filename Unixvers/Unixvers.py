import sublime
import sublime_plugin
import webbrowser

try:
    import ssl
except (ImportError):
    pass


class UnixversCommand(sublime_plugin.WindowCommand):
    lien = []
    recherche = []
    serveur = []
    social = []
    s = None
    packageUrl = None
    selection = ""

    lien = {"label": "url"}
    recherche = {"label": "url"}
    serveur = {"label": "url"}

    def __init__(self, *args, **kwargs):
        super(UnixversCommand, self).__init__(*args, **kwargs)

        s = sublime.load_settings('Unixvers.sublime-settings')
        if not s.has('social'):
            s.set('social', self.social)
        if not s.has('serveur'):
            s.set('serveur', self.serveur)
        if not s.has('recherche'):
            s.set('recherche', self.recherche)
        if not s.has('lien'):
            s.set('lien', self.lien)

        sublime.save_settings('Unixvers.sublime-settings')


    def run(self):
        self.s = sublime.load_settings('Unixvers.sublime-settings')
        self.lien = []
        self.recherche = []
        self.serveur = []
        self.social = []

        options = ['Lien', 'Recherche', 'Serveur', "Social"]

        self.window.show_quick_panel(options, self.callback)

    def callback(self, index):
        if not self.window.views():
            self.window.new_file()

        if (index == 0):
            self.list_lien()
        elif (index == 1):
            self.list_recherche()
        elif (index == 2):
            self.list_serveur() 
        elif (index == 3):
            self.list_social() 

    def list_lien(self):
        lien = self.s.get('lien')
        if not lien:
            self.s.set('lien', self.lien)
            sublime.save_settings('Unixvers.sublime-settings')
            lien = self.s.get('lien')

        for name, url in lien.iteritems():
            self.lien.append([name, url])
        
        self.window.show_quick_panel(self.lien, self.get_lien)

    def get_lien(self, index):
        if (index > -1):
            url = self.lien[index][1]
            webbrowser.open_new_tab(url)

    def list_recherche(self):
        recherche = self.s.get('recherche')
        if not recherche:
            self.s.set('recherche', self.recherche)
            sublime.save_settings('Unixvers.sublime-settings')
            recherche = self.s.get('recherche')

        for name, url in recherche.iteritems():
            self.recherche.append([name, url])

        self.window.show_quick_panel(self.recherche, self.get_recherche)

    def get_recherche(self, index):
        if (index > -1):
            url = self.recherche[index][1]
            # sublime.error_message(url )
            sublime.set_clipboard(url)
            self.window.run_command("unixvers_get_select")

    def list_serveur(self):
        serveur = self.s.get('serveur')
        if not serveur:
            self.s.set('serveur', self.serveur)
            sublime.save_settings('Unixvers.sublime-settings')
            serveur = self.s.get('serveur')

        for name, url in serveur.iteritems():
            self.serveur.append([name, url])

        self.window.show_quick_panel(self.serveur, self.get_serveur)

    def get_serveur(self, index):
        if (index > -1):
            url = self.serveur[index][1]
            sublime.set_clipboard(url)
            webbrowser.open_new_tab(url)

    def list_social(self):
        social = self.s.get('social')
        if not social:
            self.s.set('social', self.social)
            sublime.save_settings('Unixvers.sublime-settings')
            social = self.s.get('social')

        for name, url in social.iteritems():
            self.social.append([name, url])

        self.window.show_quick_panel(self.social, self.get_social)

    def get_social(self, index):
        if (index > -1):
            url = self.social[index][1]
            sublime.set_clipboard(url)
            webbrowser.open_new_tab(url)
           

class UnixversGetSelect(sublime_plugin.TextCommand):

    def run(self, edit):
        selection = ""
        for region in self.view.sel():
            selection += self.view.substr(region)
        if(selection):
            webbrowser.open_new_tab(sublime.get_clipboard()+selection)
