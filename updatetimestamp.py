import datetime
import sublime
import sublime_plugin

class UpdateTimestamp(sublime_plugin.TextCommand):
	def run(self, edit):
		settings = sublime.load_settings("updatetimestamp.sublime-settings")

		dateformat = settings.get('date_format')
		if not dateformat:
			dateformat = "%Y-%m-%d"
		now = datetime.datetime.now().strftime(dateformat)
		prefix = settings.get('prefix')
		if not prefix:
			prefix = "Last modified on: "
		
		text_to_find = "%s.*\n" % prefix
		text_to_write = "%s %s\n" % (prefix, now)

		
		region = self.view.find(text_to_find, 0)
		while region:				
			start = region.begin()
			self.view.erase(edit, region)
			self.view.insert(edit, start, text_to_write)
			next_start = start + len(text_to_write)
			region = self.view.find(text_to_find, next_start)
			

class UpdateTimestampOnSave(sublime_plugin.EventListener):

	def on_pre_save(self, view):
		settings = sublime.load_settings("updatetimestamp.sublime-settings")
		if settings.get("update_timestamp_on_save") == True:
			view.run_command("update_timestamp")
