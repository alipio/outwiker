#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
Команды для интерфейса
"""

import os.path
import shutil

import wx

import outwiker.core.exceptions
import outwiker.core.commands
from .system import getCurrentDir
from .version import Version

from tree import WikiDocument, RootWikiPage
from outwiker.gui.OverwriteDialog import OverwriteDialog
from application import Application
from outwiker.gui.about import AboutDialog
from attachment import Attachment


def MessageBox (*args, **kwargs):
	"""
	Замена стандартного MessageBox. Перед показом диалога отключает приложение от события EVT_ACTIVATE_APP.
	"""
	wx.GetApp().unbindActivateApp()
	result = wx.MessageBox (*args, **kwargs)
	wx.GetApp().bindActivateApp()

	return result


def testreadonly (func):
	"""
	Декоратор для отлавливания исключения outwiker.core.exceptions.ReadonlyException
	"""
	def readOnlyWrap (*args, **kwargs):
		try:
			func (*args, **kwargs)
		except outwiker.core.exceptions.ReadonlyException:
			MessageBox (_(u"Wiki is opened as read-only"), _(u"Error"), wx.ICON_ERROR | wx.OK)

	return readOnlyWrap


@testreadonly
def attachFilesWithDialog (parent, page):
	"""
	Вызвать диалог для приаттачивания файлов к странице
	parent - родительское окно
	page - страница, куда прикрепляем файлы
	"""
	if page.readonly:
		raise outwiker.core.exceptions.ReadonlyException

	dlg = wx.FileDialog (parent, style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_MULTIPLE)

	if dlg.ShowModal() == wx.ID_OK:
		files = dlg.GetPaths()
		files.sort()
		attachFiles (parent, page, files)

	dlg.Destroy()


@testreadonly
def attachFiles (parent, page, files):
	"""
	Прикрепить файлы к странице с диалогом о перезаписи при необходимости
	parent - родительское окно
	page - страница, куда прикрепляем файлы
	"""
	if page.readonly:
		raise outwiker.core.exceptions.ReadonlyException

	oldAttaches = [os.path.basename (fname).lower() for fname in Attachment (page).attachmentFull]

	with OverwriteDialog (parent) as overwriteDialog:
		for fname in files:
			if os.path.basename (fname).lower() in oldAttaches:
				text = _(u"File '%s' exists already") % (os.path.basename (fname))
				result = overwriteDialog.ShowDialog (text)

				if result == overwriteDialog.ID_SKIP:
					continue
				elif result == wx.ID_CANCEL:
					break
			
			try:
				Attachment (page).attach ([fname])
			except IOError:
				text = u'Can\'t attach file "%s"' % (fname)
				MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)
			except shutil.Error:
				text = u'Can\'t attach file "%s"' % (fname)
				MessageBox (text, _(u"Error"), wx.ICON_ERROR | wx.OK)


@testreadonly
def removePage (page):
	if page.readonly:
		raise outwiker.core.exceptions.ReadonlyException

	text = _(u"Remove page '%s' and all subpages?") % (page.title)

	if MessageBox (text, _(u"Remove page?"), wx.YES_NO  | wx.ICON_QUESTION) == wx.YES:
		root = page.root
		Application.onStartTreeUpdate(root)

		try:
			page.remove()
		except IOError:
			MessageBox (_(u"Can't remove page"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		finally:
			Application.onEndTreeUpdate(root)



def openWikiWithDialog (parent, readonly=False):
	"""
	Показать диалог открытия вики и вернуть открытую wiki
	parent -- родительское окно
	"""
	wikiroot = None

	dialog = wx.FileDialog (parent, 
			wildcard = "__page.opt|__page.opt", 
			style = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)

	if dialog.ShowModal() == wx.ID_OK:
		fullpath = dialog.GetPath()
		path = os.path.dirname(fullpath)
		wikiroot = openWiki (path, readonly)

	dialog.Destroy()

	return wikiroot


def openWiki (path, readonly=False):
	wikiroot = None

	Application.onStartTreeUpdate(None)
	
	try:
		# Загрузить вики
		wikiroot = WikiDocument.load (os.path.realpath (path), readonly)
		Application.wikiroot = wikiroot
	except IOError:
		__canNotLoadWikiMessage (path)

	except outwiker.core.exceptions.RootFormatError:
		__rootFormatErrorHandle(path, readonly)

	finally:
		Application.onEndTreeUpdate(wikiroot)

	return Application.wikiroot


def __rootFormatErrorHandle (path, readonly):
	"""
	Обработчик исключения outwiker.core.exceptions.RootFormatError
	"""
	if readonly:
		# Если вики открыт только для чтения, то нельзя изменять файлы
		__canNotLoadWikiMessage (path)
		return

	if (__wantClearWikiOptions (path) != wx.YES):
		return

	# Обнулим файл __page.opt
	WikiDocument.clearConfigFile (path)

	# Попробуем открыть вики еще раз
	try:
		# Загрузить вики
		wikiroot = WikiDocument.load (os.path.realpath (path), readonly)
		Application.wikiroot = wikiroot
	except IOError:
		__canNotLoadWikiMessage (path)

	except outwiker.core.exceptions.RootFormatError:
		__canNotLoadWikiMessage (path)

	finally:
		pass


def __canNotLoadWikiMessage (path):
	"""
	Вывести сообщение о том, что невоможно открыть вики
	"""
	outwiker.core.commands.MessageBox (_(u"Can't load wiki '%s'") % path, 
				_(u"Error"), 
				wx.ICON_ERROR | wx.OK)


def __wantClearWikiOptions (path):
	"""
	Сообщение о том, хочет ли пользователь сбросить файл __page.opt
	"""
	return outwiker.core.commands.MessageBox (_(u"Can't load wiki '%s'\nFile __page.opt is invalid.\nClear this file and load wiki?\nBookmarks will be lost") % path, 
				_(u"__page.opt error"), 
				wx.ICON_ERROR | wx.YES_NO)


def createNewWiki (parentwnd):
	"""
	Создать новую вики
	parentwnd - окно-владелец диалога выбора файла
	"""
	dlg = wx.FileDialog (parentwnd, style = wx.FD_SAVE)

	if dlg.ShowModal() == wx.ID_OK:
		try:
			Application.wikiroot = WikiDocument.create (dlg.GetPath ())
			Application.wikiroot.selectedPage = None
		except (IOError, OSError) as e:
			# TODO: проверить под Windows
			outwiker.core.commands.MessageBox (_(u"Can't create wiki\n") + unicode (str (e), "utf8"),
					_(u"Error"), wx.OK | wx.ICON_ERROR)

	dlg.Destroy()


def copyTextToClipboard (text):
	if not wx.TheClipboard.Open():
		MessageBox (_(u"Can't open clipboard"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	data = wx.TextDataObject (text)

	if not wx.TheClipboard.SetData(data):
		MessageBox (_(u"Can't copy text to clipboard"), _(u"Error"), wx.ICON_ERROR | wx.OK)

	wx.TheClipboard.Flush()
	wx.TheClipboard.Close()


def copyPathToClipboard (page):
	"""
	Копировать путь до страницы в буфер обмена
	"""
	assert page != None
	copyTextToClipboard (page.path)


# TODO: Сделать тест
def copyAttachPathToClipboard (page):
	"""
	Копировать путь до папки с прикрепленными файлами в буфер обмена
	"""
	assert page != None
	copyTextToClipboard (Attachment(page).getAttachPath(create=True))


def copyLinkToClipboard (page):
	"""
	Копировать ссылку на страницу в буфер обмена
	"""
	assert page != None
	copyTextToClipboard ("/" + page.subpath)


def copyTitleToClipboard (page):
	"""
	Копировать заголовок страницы в буфер обмена
	"""
	assert page != None
	copyTextToClipboard (page.title)


@testreadonly
def movePage (page, newParent):
	"""
	Сделать страницу page ребенком newParent
	"""
	assert page != None
	assert newParent != None

	try:
		page.moveTo (newParent)
	except outwiker.core.exceptions.DublicateTitle:
		# Невозможно переместить из-за дублирования имен
		MessageBox (_(u"Can't move page when page with that title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)
	except outwiker.core.exceptions.TreeException:
		# Невозможно переместить по другой причине
		MessageBox (_(u"Can't move page"), _(u"Error"), wx.ICON_ERROR | wx.OK)


def setStatusText (text, index = 0):
	"""
	Установить текст статусбара.
	text - текст
	index - номер ячейки статусбара
	"""
	Application.mainWindow.statusbar.SetStatusText (text, index)


def getCurrentVersion ():
	fname = "version.txt"
	path = os.path.join (outwiker.core.system.getCurrentDir(), fname)

	try:
		with open (path) as fp:
			lines = fp.readlines()
	except IOError, e:
		MessageBox (_(u"Can't open file %s") % fname, _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	version_str = "%s.%s %s" % (lines[0].strip(), lines[1].strip(), lines[2].strip())

	try:
		version = Version.parse (version_str)
	except ValueError:
		MessageBox (_(u"Can't parse version"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		version = Version(0, 0)

	return version


@testreadonly
def moveCurrentPageUp ():
	"""
	Переместить текущую страницу на одну позицию вверх
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		Application.wikiroot.selectedPage.order -= 1


@testreadonly
def moveCurrentPageDown ():
	"""
	Переместить текущую страницу на одну позицию вниз
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		Application.wikiroot.selectedPage.order += 1


@testreadonly
def sortChildrenAlphabeticalGUI ():
	"""
	Команда для сортировки дочерних страниц текущей страницы по алфавиту
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		Application.wikiroot.selectedPage.sortChildrenAlphabetical ()
	else:
		Application.wikiroot.sortChildrenAlphabetical ()


@testreadonly
def sortSiblingsAlphabeticalGUI ():
	"""
	Команда для сортировки по алфавиту того же уровня, на котором мы сейчас находимся
	"""
	if Application.wikiroot == None:
		MessageBox (_(u"Wiki is not open"), _(u"Error"), wx.ICON_ERROR | wx.OK)
		return

	if Application.wikiroot.selectedPage != None:
		Application.wikiroot.selectedPage.parent.sortChildrenAlphabetical ()


@testreadonly
def renamePage (page, newtitle):
	try:
		page.title = newtitle
		#page.root.selectedPage = page

	except outwiker.core.exceptions.DublicateTitle:
		outwiker.core.commands.MessageBox (_(u"Can't move page when page with that title already exists"), _(u"Error"), wx.ICON_ERROR | wx.OK)

	except OSError as e:
		outwiker.core.commands.MessageBox (_(u"Can't rename page\n%s") % unicode (e), _(u"Error"), wx.ICON_ERROR | wx.OK)


def showAboutDialog (parent):
	version = getCurrentVersion()
	dlg = AboutDialog (version, parent)
	dlg.ShowModal()
	dlg.Destroy()


def openHelp ():
	help_dir = u"help"
	current_help = _("help_en")
	path = os.path.join (outwiker.core.system.getCurrentDir(), help_dir, current_help)
	outwiker.core.commands.openWiki (path, readonly=True)


def reloadWiki (mainWnd):
	"""
	Перезагрузить вики
	mainWnd - указатель на главное окно. Нужно, чтобы сообщить ему о необходимости удалить панель с текущей страницей
	"""
	if Application.wikiroot != None:
		result = (outwiker.core.commands.MessageBox (_(u"Save current page before reload?"), 
			_(u"Save?"), wx.YES_NO | wx.CANCEL  | wx.ICON_QUESTION ))

		if result == wx.CANCEL:
			return

		mainWnd.destroyPagePanel (result == wx.YES)
		outwiker.core.commands.openWiki (Application.wikiroot.path)