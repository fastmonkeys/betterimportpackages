import shutil
import os.path
import sublime
import sublime_plugin

from subprocess import Popen, PIPE


ACK_PATHS = [
    shutil.which('ack'),
    '/usr/bin/ack',
    '/usr/local/bin/ack'
]

for path in ACK_PATHS:
    if path and os.path.isfile(path):
        ACK_PATH = path
        break
else:
    ACK_PATH = None


def analyze_data(data, word):
    best_match = []
    from_module = None
    import_what = None
    for line in data.replace("\r", "").split("\n"):
        if line.startswith('from '):
            from_module = line.split(' ')[1]
            import_what = word
        elif line.startswith('import '):
            from_module = line.split(' ')[1]
            import_what = None
        elif line == '':
            from_module = None
            import_what = None

        if word in line and from_module:
            best_match.append((from_module, import_what))

    best_match.sort(key=lambda x: 1 if x[0].startswith('.') else 0)
    if best_match:
        return best_match[0]

    return None


# SafetyReview
class InsertimportCommand(sublime_plugin.TextCommand):
    def find_first_import(self):
        first_import = self.view.find('^(from|import)', 0)
        if first_import:
            return first_import.a

    def find_end_of_comments(self):
        end_of_comments = self.view.find('^#(.*)$', 0)
        if end_of_comments:
            return end_of_comments.b+1

    def find_insert_position(self):
        for x in [
            self.find_first_import,
            self.find_end_of_comments,
            lambda: 0
        ]:
            a = x()
            if a:
                return a

    def run(self, edit, analyzed):
        import_position = self.find_insert_position()

        if analyzed[0] and analyzed[1]:
            self.view.insert(edit, import_position, "from %s import %s\n" % (
                analyzed[0],
                analyzed[1]
            ))
        elif analyzed[0]:
            self.view.insert(edit, import_position, "import %s\n" % (
                analyzed[0]
            ))


class ImportifyCommand(sublime_plugin.TextCommand):
    def search_project_for_import(self, word):
        # This is a huge hack.
        if not ACK_PATH:
            sublime.error_message("Could not find ack binary.")

        folders = sublime.active_window().folders()
        for folder in folders:
            data = Popen([
                ACK_PATH,
                '-B6',
                '--no-filename',
                '--python',
                word,
                folder
            ], stdout=PIPE, stderr=PIPE).communicate()[0].decode('utf-8')
            analyzed = analyze_data(data, word)
            if analyzed:
                return analyzed

        return None

    def add_import(self, data):
        analyzed = self.search_project_for_import(data)
        if analyzed:
            self.view.window().run_command(
                'insertimport',
                {'analyzed': analyzed}
            )
        else:
            sublime.error_message("Could not find import for %r" % data)

    def run(self, edit, **kwargs):
        for region in self.view.sel():
            region = self.view.word(region)
            if not region.empty():
                data = self.view.substr(region)
                sublime.set_timeout_async(lambda: self.add_import(data), 0)
