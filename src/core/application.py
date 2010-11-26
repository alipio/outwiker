#!/usr/bin/env python
#-*- coding: utf-8 -*-

import gettext

from core.config import GeneralConfig, getConfigPath
import core.i18n

class Application (object):
	def __init__ (self, configFilename):
		pass

	
	@staticmethod
	def init (configFilename):
		Application.config = GeneralConfig (configFilename)
		Application.__initLocale()


	@staticmethod
	def __initLocale ():
		language = Application.config.languageOption.value

		try:
			core.i18n.init_i18n (language)
		except IOError, e:
			#wx.MessageBox (u"Can't load language: %s" % language, u"Error", wx.ICON_ERROR | wx.OK) 
			print u"Can't load language: %s" % language