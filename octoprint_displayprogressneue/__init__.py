# coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import octoprint.events
import time

class DisplayProgressNeuePlugin(octoprint.plugin.ProgressPlugin,
                            octoprint.plugin.EventHandlerPlugin,
                            octoprint.plugin.SettingsPlugin):

	##~~ SettingsPlugin

	def get_settings_defaults(self):
		return dict(
			message="{bar} {progress:>3}%",
			marlin_bar=True
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		return dict(
			displayprogress_neue=dict(
				displayName="DisplayProgress Neue",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="juniorRubyist",
				repo="OctoPrint-DisplayProgressNeue",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/OctoPrint/OctoPrint-DisplayProgressNeue/archive/{target_version}.zip"
			)
		)

	##~~ EventHandlerPlugin

	def on_event(self, event, payload):
		if event == octoprint.events.Events.PRINT_STARTED:
			self._send_message(payload["origin"], payload["path"], 0)
		elif event == octoprint.events.Events.PRINT_DONE:
			self._send_message(payload["origin"], payload["path"], 100)

	##~~ ProgressPlugin

	def on_print_progress(self, storage, path, progress):
		if not self._printer.is_printing():
			return
		self._send_message(storage, path, progress)

	##~~ helpers

	def _send_message(self, storage, path, progress):
		marlin_bar = self._settings.get(["marlin_bar"])
		message = self._settings.get(["message"]).format(progress=progress,
		                                                 storage=storage,
		                                                 path=path,
		                                                 bar=self.__class__._progress_bar(progress),
														 time=self.__class__.time_string()
														)
		self._printer.commands("M117 {}".format(message))
		if marlin_bar:
			self._printer.commands("M73 P{progress}".format(progress=progress))

	@classmethod
	def _progress_bar(cls, progress):
		hashes = "#" * int(round(progress / 10))
		spaces = " " * (10 - len(hashes))
		return "[{}{}]".format(hashes, spaces)
	
	@classmethod
	def _time_string(cls):
		t = time.localtime()
		return "{h}:{m} {a}".format(h="0{h}".format(h=(12 if t.tm_hour%12==0 else t.tm_hour%12))[-2:], m="0{m}".format(m=t.tm_min)[-2:], a=("PM" if t.tm_hour/12 else "AM"))

__plugin_name__ = "DisplayProgress Neue"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = DisplayProgressNeuePlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

