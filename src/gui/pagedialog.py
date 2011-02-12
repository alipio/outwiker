# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Wed Apr 07 20:05:46 2010

import wx

from core.search import TagsList
from core.tree import RootWikiPage
import core.commands
from core.application import Application
from gui.BasePageDialog import BasePageDialog
import core.factory


@core.commands.testreadonly
def editPage (parentWnd, currentPage):
	"""
	Вызвать диалог для редактирования страницы
	parentWnd - родительское окно
	currentPage - страница для редактирования
	"""
	if currentPage.readonly:
		raise core.exceptions.ReadonlyException

	dlg = EditPageDialog (currentPage, currentPage.parent, parent = parentWnd)
	page = None

	if dlg.ShowModal() == wx.ID_OK:
		Application.onStartTreeUpdate(currentPage.root)

		try:
			factory = dlg.selectedFactory
			tags = dlg.tags

			currentPage.tags = dlg.tags
			currentPage.icon = dlg.icon

			try:
				currentPage.title = dlg.pageTitle
			except OSError as e:
				MessageBox (_(u"Can't rename page\n") + unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)

			currentPage.root.selectedPage = currentPage
		finally:
			Application.onEndTreeUpdate(currentPage.root)

	dlg.Destroy()


@core.commands.testreadonly
def createPageWithDialog (parentwnd, parentpage):
	"""
	Показать диалог настроек и создать страницу
	"""
	if parentpage.readonly:
		raise core.exceptions.ReadonlyException
	
	dlg = CreatePageDialog (parentpage, parentwnd)
	page = None

	if dlg.ShowModal() == wx.ID_OK:
		factory = dlg.selectedFactory
		title = dlg.pageTitle
		tags = dlg.tags

		Application.onStartTreeUpdate(parentpage.root)

		try:
			page = factory.create (parentpage, title, tags)
			
			assert page != None

			page.icon = dlg.icon
			page.root.selectedPage = page

		except OSError, IOError:
			MessageBox (_(u"Can't create page"), "Error", wx.ICON_ERROR | wx.OK)
		finally:
			Application.onEndTreeUpdate(parentpage.root)

	dlg.Destroy()


	return page


def createSiblingPage (parentwnd):
	"""
	Создать страницу, находящуюся на том же уровне, что и текущая страница
	parentwnd - окно, которое будет родителем для диалога создания страницы
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	currPage = Application.wikiroot.selectedPage

	if currPage == None or currPage.parent == None:
		parentpage = Application.wikiroot
	else:
		parentpage = currPage.parent

	createPageWithDialog (parentwnd, parentpage)


def createChildPage (parentwnd):
	"""
	Создать страницу, которая будет дочерней к текущей странице
	parentwnd - окно, которое будет родителем для диалога создания страницы
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	currPage = Application.wikiroot.selectedPage

	if currPage == None:
		currPage = Application.wikiroot

	createPageWithDialog (parentwnd, currPage)


class CreatePageDialog (BasePageDialog):
	def __init__ (self, parentPage = None, *args, **kwds):
		BasePageDialog.__init__ (self, parentPage, *args, **kwds)

		if parentPage.parent != None:
			tags = TagsList.getTagsString (parentPage.tags)
			self.tagsTextCtrl.SetValue (tags)
	

	def onOk (self, event):
		if not self.testPageTitle (self.pageTitle):
			core.commands.MessageBox (_(u"Invalid page title"), _(u"Error"), wx.ICON_ERROR | wx.OK)
			return

		if self.parentPage != None and \
				not RootWikiPage.testDublicate(self.parentPage, self.pageTitle):
			core.commands.MessageBox (_(u"A page with this title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)
			return

		event.Skip()


class EditPageDialog (BasePageDialog):
	def __init__ (self, currentPage, parentPage = None, *args, **kwds):
		BasePageDialog.__init__ (self, parentPage, *args, **kwds)

		assert currentPage != None
		self.currentPage = currentPage

		self.SetTitle(_(u"Edit page properties"))
		self._prepareForChange (currentPage)


	def _prepareForChange (self, currentPage):
		"""
		Подготовить диалог к редактированию свойств страницы
		"""
		tags = TagsList.getTagsString (currentPage.tags)
		self.tagsTextCtrl.SetValue (tags)
		
		# Запретить изменять заголовок
		self.titleTextCtrl.SetValue (currentPage.title)

		# Установить тип страницы
		self._setPageType(currentPage)

		# Добавить текущую иконку
		icon = currentPage.icon
		if icon != None:
			index = self.icons.Add (wx.Bitmap (icon) )
			selItem = self.iconsList.InsertImageStringItem (len (self.iconsDict) - 1, _(u"Current icon"), index)
			self.iconsList.SetItemState (selItem, wx.LIST_STATE_SELECTED, wx.LIST_STATE_SELECTED)
			self.iconsDict[selItem] = icon


	def _setPageType (self, currentPage):
		"""
		Установить тип страницы в диалоге
		"""
		n = 0
		for factory in core.factory.FactorySelector.factories:
			if factory.getTypeString() == core.factory.FactorySelector.getFactory(currentPage.type).getTypeString():
				self.comboType.SetSelection (n)
				self.comboType.Disable ()
				break
			n += 1
	

	def onOk (self, event):
		if not self.testPageTitle (self.pageTitle):
			core.commands.MessageBox (_(u"Invalid page title"), _(u"Error"), wx.ICON_ERROR | wx.OK)
			return

		if not self.currentPage.canRename (self.pageTitle):
			core.commands.MessageBox (_(u"Can't rename page when page with that title already exists"), 
					_(u"Error"), 
					wx.ICON_ERROR | wx.OK)
			return

		event.Skip()
