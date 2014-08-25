import sublime, sublime_plugin
import os
import tempfile
import subprocess
import desktop

settings = sublime.load_settings('SeqdiagPreview.sublime-settings')


def getTempPreviewPath(view):
	" return a permanent full path of the temp preview file "
	tmp_filename = 'seqdiag_preview_%s.png' % view.id()
	tmp_fullpath = os.path.join(tempfile.gettempdir(), tmp_filename)
	return tmp_fullpath


def encodeFilePath(path):
	" encode file path for each platforms encoding "
	if sublime.platform() == 'windows':
		return path.encode('cp932')
	return path.encode('utf_8')


class SeqdiagPreviewListener(sublime_plugin.EventListener):
	def on_post_save(self, view):
		if view.file_name().endswith('.diag'):
			temp_file = getTempPreviewPath(view)
			if os.path.isfile(temp_file):
				# reexec conversion
				view.run_command('seqdiag_preview', {'open': settings.get('open_on_save', false)})
				sublime.status_message('Seqdiag preview file updated')


class SeqdiagPreviewCommand(sublime_plugin.TextCommand):
	def run(self, edit, open=True):
		temp = encodeFilePath(getTempPreviewPath(self.view))
		source = encodeFilePath(self.view.file_name())
		retcode = subprocess.call(['seqdiag', source, '-o', temp])
		if retcode < 0:
			msg = 'Seqdiag process is failed!'
			print msg
			sublime.status_message(msg)
		elif open:
			desktop.open(temp)

