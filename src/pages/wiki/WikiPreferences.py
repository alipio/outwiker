#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed Nov 24 21:52:16 2010

import wx

from gui.preferences.ConfigElements import BooleanElement
#from wikipage import WikiPageFactory
import wikipage

# begin wxGlade: extracode
# end wxGlade



class WikiPrefGeneralPanel(wx.Panel):
	def __init__(self, *args, **kwds):
		# begin wxGlade: WikiPrefGeneralPanel.__init__
		kwds["style"] = wx.TAB_TRAVERSAL
		wx.Panel.__init__(self, *args, **kwds)
		self.htmlCodeCheckbox = wx.CheckBox(self, -1, _("Show HTML Code Tab"))

		self.__set_properties()
		self.__do_layout()
		# end wxGlade

	def __set_properties(self):
		# begin wxGlade: WikiPrefGeneralPanel.__set_properties
		pass
		# end wxGlade

	def __do_layout(self):
		# begin wxGlade: WikiPrefGeneralPanel.__do_layout
		mainSizer = wx.FlexGridSizer(2, 1, 0, 0)
		mainSizer.Add(self.htmlCodeCheckbox, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 2)
		self.SetSizer(mainSizer)
		mainSizer.Fit(self)
		mainSizer.AddGrowableCol(0)
		# end wxGlade
	

	def LoadState(self):
		# Показывать ли вкладку с кодом HTML?
		self.showHtmlCode = BooleanElement (wikipage.WikiPageFactory.showHtmlCodeOptions, self.htmlCodeCheckbox)
	

	def Save (self):
		changed = self.showHtmlCode.isValueChanged()

		self.showHtmlCode.save()

		if changed:
			currpage = wx.GetApp().GetTopWindow().wikiroot.selectedPage
			wx.GetApp().GetTopWindow().wikiroot.selectedPage = None
			wx.GetApp().GetTopWindow().wikiroot.selectedPage = currpage

# end of class WikiPrefGeneralPanel

