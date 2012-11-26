import sublime, sublime_plugin
import os
import tempfile
import subprocess
import desktop

# TODO getTempPreviewPath を何度も使うのが微妙 
# TODO blockdiagコマンドは内蔵させる？

def getTempPreviewPath(view):
	" return a permanent full path of the temp preview file "
	tmp_filename = 'blockdiag_preview_%s.png' % view.id()
	tmp_fullpath = os.path.join(tempfile.gettempdir(), tmp_filename)
	return tmp_fullpath

class BlockdiagPreviewListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if view.file_name().endswith('.diag'):
			temp_file = getTempPreviewPath(view)
			if os.path.isfile(temp_file):
				# reexec conversion
				view.run_command('blockdiag_preview', {'path': temp_file})
				sublime.status_message('Blockdiag preview file updated')

class BlockdiagPreviewCommand(sublime_plugin.TextCommand):
	def run(self, edit, path=''):
		if len(path) == 0:
			path = getTempPreviewPath(self.view)
		retcode = subprocess.call(['blockdiag', self.view.file_name(), '-o', path])
		if retcode < 0:
			sublime.status_message('error!')
		else:
			desktop.open(path)
