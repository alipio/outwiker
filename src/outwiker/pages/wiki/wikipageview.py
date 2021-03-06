# -*- coding: UTF-8 -*-

import wx
import os

from .wikieditor import WikiEditor
from .wikitoolbar import WikiToolBar

from .wikiconfig import WikiConfig
from .htmlgenerator import HtmlGenerator
from .htmlcache import HtmlCache

from outwiker.actions.polyactionsid import *
from outwiker.core.commands import insertCurrentDate

from actions.fontsizebig import WikiFontSizeBigAction
from actions.fontsizesmall import WikiFontSizeSmallAction
from actions.nonparsed import WikiNonParsedAction
from actions.thumb import WikiThumbAction
from actions.link import insertLink
from actions.equation import WikiEquationAction
from actions.attachlist import WikiAttachListAction
from actions.childlist import WikiChildListAction
from actions.include import WikiIncludeAction
from actions.dates import WikiDateCreationAction, WikiDateEditionAction

from .basewikipageview import BaseWikiPageView


class WikiPageView (BaseWikiPageView):
    def __init__ (self, parent, *args, **kwds):
        super (WikiPageView, self).__init__ (parent, *args, **kwds)


    def Clear (self):
        super (WikiPageView, self).Clear ()


    def _getHtmlGenerator (self, page):
        return HtmlGenerator (page)


    def getTextEditor(self):
        return WikiEditor


    def _getName (self):
        return u"wiki"


    def _getPageTitle (self):
        return _(u"Wiki")


    def _getMenuTitle (self):
        return _(u"Wiki")


    def _isHtmlCodeShown (self):
        return WikiConfig (self._application.config).showHtmlCodeOptions.value


    def _createToolbar (self, mainWindow):
        return WikiToolBar(mainWindow, mainWindow.auiManager)


    def _getCacher (self, page, application):
        return HtmlCache (page, application)


    @property
    def commandsMenu (self):
        """
        Свойство возвращает меню с викикомандами
        """
        return self._commandsMenu


    def _getPolyActions (self):
        return [
            BOLD_STR_ID,
            ITALIC_STR_ID,
            BOLD_ITALIC_STR_ID,
            UNDERLINE_STR_ID,
            STRIKE_STR_ID,
            SUBSCRIPT_STR_ID,
            SUPERSCRIPT_STR_ID,
            QUOTE_STR_ID,
            ALIGN_LEFT_STR_ID,
            ALIGN_CENTER_STR_ID,
            ALIGN_RIGHT_STR_ID,
            ALIGN_JUSTIFY_STR_ID,
            HEADING_1_STR_ID,
            HEADING_2_STR_ID,
            HEADING_3_STR_ID,
            HEADING_4_STR_ID,
            HEADING_5_STR_ID,
            HEADING_6_STR_ID,
            PREFORMAT_STR_ID,
            CODE_STR_ID,
            ANCHOR_STR_ID,
            HORLINE_STR_ID,
            LINK_STR_ID,
            LIST_BULLETS_STR_ID,
            LIST_NUMBERS_STR_ID,
            LINE_BREAK_STR_ID,
            HTML_ESCAPE_STR_ID,
            CURRENT_DATE,
        ]


    def _getSpecificActions (self):
        return [
            WikiFontSizeBigAction,
            WikiFontSizeSmallAction,
            WikiNonParsedAction,
            WikiThumbAction,
            WikiEquationAction,
            WikiAttachListAction,
            WikiChildListAction,
            WikiIncludeAction,
            WikiDateCreationAction,
            WikiDateEditionAction
        ]


    def _createWikiTools (self):
        assert self.mainWindow is not None

        self._headingMenu = wx.Menu()
        self._fontMenu = wx.Menu()
        self._alignMenu = wx.Menu()
        self._formatMenu = wx.Menu()
        self._listMenu = wx.Menu()
        self._commandsMenu = wx.Menu()

        self.toolsMenu.AppendSeparator()

        self.toolsMenu.AppendSubMenu (self._headingMenu, _(u"Heading"))
        self.toolsMenu.AppendSubMenu (self._fontMenu, _(u"Font"))
        self.toolsMenu.AppendSubMenu (self._alignMenu, _(u"Alignment"))
        self.toolsMenu.AppendSubMenu (self._formatMenu, _(u"Formatting"))
        self.toolsMenu.AppendSubMenu (self._listMenu, _(u"Lists"))
        self.toolsMenu.AppendSubMenu (self._commandsMenu, _(u"Commands"))

        self.__addCommandsTools()
        self.__addFontTools()
        self.__addAlignTools()
        self.__addHTools()
        self.__addListTools()
        self.__addFormatTools()
        self.__addOtherTools()


    def __addCommandsTools (self):
        # Команда (:attachlist:)
        self._application.actionController.appendMenuItem (WikiAttachListAction.stringId, self.commandsMenu)

        # Команда (:childlist:)
        self._application.actionController.appendMenuItem (WikiChildListAction.stringId, self.commandsMenu)

        # Команда (:include:)
        self._application.actionController.appendMenuItem (WikiIncludeAction.stringId, self.commandsMenu)

        # Команда (:crdate:))
        self._application.actionController.appendMenuItem (WikiDateCreationAction.stringId, self.commandsMenu)

        # Команда (:eddate:))
        self._application.actionController.appendMenuItem (WikiDateEditionAction.stringId, self.commandsMenu)


    def __addFontTools (self):
        """
        Добавить инструменты, связанные со шрифтами
        """
        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self._fontMenu

        # Полужирный шрифт
        self._application.actionController.getAction (BOLD_STR_ID).setFunc (lambda param: self.turnText (u"'''", u"'''"))

        self._application.actionController.appendMenuItem (BOLD_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_bold.png"),
                                                                fullUpdate=False)


        # Курсивный шрифт
        self._application.actionController.getAction (ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"''", u"''"))

        self._application.actionController.appendMenuItem (ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ITALIC_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_italic.png"),
                                                                fullUpdate=False)

        # Полужирный курсивный шрифт
        self._application.actionController.getAction (BOLD_ITALIC_STR_ID).setFunc (lambda param: self.turnText (u"''''", u"''''"))

        self._application.actionController.appendMenuItem (BOLD_ITALIC_STR_ID, menu)
        self._application.actionController.appendToolbarButton (BOLD_ITALIC_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_bold_italic.png"),
                                                                fullUpdate=False)


        # Подчеркнутый шрифт
        self._application.actionController.getAction (UNDERLINE_STR_ID).setFunc (lambda param: self.turnText (u"{+", u"+}"))

        self._application.actionController.appendMenuItem (UNDERLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (UNDERLINE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_underline.png"),
                                                                fullUpdate=False)


        # Зачеркнутый шрифт
        self._application.actionController.getAction (STRIKE_STR_ID).setFunc (lambda param: self.turnText (u"{-", u"-}"))

        self._application.actionController.appendMenuItem (STRIKE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (STRIKE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_strikethrough.png"),
                                                                fullUpdate=False)


        # Нижний индекс
        self._application.actionController.getAction (SUBSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"'_", u"_'"))

        self._application.actionController.appendMenuItem (SUBSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUBSCRIPT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_subscript.png"),
                                                                fullUpdate=False)


        # Верхний индекс
        self._application.actionController.getAction (SUPERSCRIPT_STR_ID).setFunc (lambda param: self.turnText (u"'^", u"^'"))

        self._application.actionController.appendMenuItem (SUPERSCRIPT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (SUPERSCRIPT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_superscript.png"),
                                                                fullUpdate=False)


        # Крупный шрифт
        self._application.actionController.appendMenuItem (WikiFontSizeBigAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiFontSizeBigAction.stringId,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_big.png"),
                                                                fullUpdate=False)


        # Мелкий шрифт
        self._application.actionController.appendMenuItem (WikiFontSizeSmallAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiFontSizeSmallAction.stringId,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_small.png"),
                                                                fullUpdate=False)


    def __addAlignTools (self):
        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self._alignMenu

        # Выравнивание по левому краю
        self._application.actionController.getAction (ALIGN_LEFT_STR_ID).setFunc (lambda param: self.turnText (u"%left%", u""))

        self._application.actionController.appendMenuItem (ALIGN_LEFT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_LEFT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_left.png"),
                                                                fullUpdate=False)


        # Выравнивание по центру
        self._application.actionController.getAction (ALIGN_CENTER_STR_ID).setFunc (lambda param: self.turnText (u"%center%", u""))

        self._application.actionController.appendMenuItem (ALIGN_CENTER_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_CENTER_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_center.png"),
                                                                fullUpdate=False)


        # Выравнивание по правому краю
        self._application.actionController.getAction (ALIGN_RIGHT_STR_ID).setFunc (lambda param: self.turnText (u"%right%", u""))

        self._application.actionController.appendMenuItem (ALIGN_RIGHT_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_RIGHT_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_right.png"),
                                                                fullUpdate=False)


        # Выравнивание по ширине
        self._application.actionController.getAction (ALIGN_JUSTIFY_STR_ID).setFunc (lambda param: self.turnText (u"%justify%", u""))

        self._application.actionController.appendMenuItem (ALIGN_JUSTIFY_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ALIGN_JUSTIFY_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_align_justify.png"),
                                                                fullUpdate=False)


    def __addHTools (self):
        """
        Добавить инструменты для заголовочных тегов <H>
        """
        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self._headingMenu

        self._application.actionController.getAction (HEADING_1_STR_ID).setFunc (lambda param: self.turnText (u"!! ", u""))
        self._application.actionController.getAction (HEADING_2_STR_ID).setFunc (lambda param: self.turnText (u"!!! ", u""))
        self._application.actionController.getAction (HEADING_3_STR_ID).setFunc (lambda param: self.turnText (u"!!!! ", u""))
        self._application.actionController.getAction (HEADING_4_STR_ID).setFunc (lambda param: self.turnText (u"!!!!! ", u""))
        self._application.actionController.getAction (HEADING_5_STR_ID).setFunc (lambda param: self.turnText (u"!!!!!! ", u""))
        self._application.actionController.getAction (HEADING_6_STR_ID).setFunc (lambda param: self.turnText (u"!!!!!!! ", u""))

        self._application.actionController.appendMenuItem (HEADING_1_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_1_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_1.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_2_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_2_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_2.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_3_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_3_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_3.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_4_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_4_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_4.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_5_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_5_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_5.png"),
                                                                fullUpdate=False)

        self._application.actionController.appendMenuItem (HEADING_6_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HEADING_6_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_heading_6.png"),
                                                                fullUpdate=False)


    def __addListTools (self):
        """
        Добавить инструменты, связанные со списками
        """
        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self._listMenu

        # Ненумерованный список
        self._application.actionController.getAction (LIST_BULLETS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList ("* "))

        self._application.actionController.appendMenuItem (LIST_BULLETS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_BULLETS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_bullets.png"),
                                                                fullUpdate=False)


        # Нумерованный список
        self._application.actionController.getAction (LIST_NUMBERS_STR_ID).setFunc (lambda param: self._application.mainWindow.pagePanel.pageView.codeEditor.turnList ("# "))

        self._application.actionController.appendMenuItem (LIST_NUMBERS_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LIST_NUMBERS_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_list_numbers.png"),
                                                                fullUpdate=False)


    def __addFormatTools (self):
        menu = self._formatMenu
        toolbar = self.mainWindow.toolbars[self._getName()]

        # Текст, который не нужно разбирать википарсером
        self._application.actionController.appendMenuItem (WikiNonParsedAction.stringId, menu)

        # Форматированный текст
        self._application.actionController.getAction (PREFORMAT_STR_ID).setFunc (lambda param: self.turnText (u"[@", u"@]"))
        self._application.actionController.appendMenuItem (PREFORMAT_STR_ID, menu)

        # Цитата
        self._application.actionController.getAction (QUOTE_STR_ID).setFunc (lambda param: self.turnText (u'[>', u'<]'))

        self._application.actionController.appendMenuItem (QUOTE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (QUOTE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "quote.png"),
                                                                fullUpdate=False)


        # Моноширинный шрифт
        self._application.actionController.getAction (CODE_STR_ID).setFunc (lambda param: self.turnText (u'@@', u'@@'))

        self._application.actionController.appendMenuItem (CODE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (CODE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "code.png"),
                                                                fullUpdate=False)


    def __addOtherTools (self):
        """
        Добавить остальные инструменты
        """
        # Добавить миниатюру
        toolbar = self.mainWindow.toolbars[self._getName()]
        menu = self.toolsMenu

        self._application.actionController.appendMenuItem (WikiThumbAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiThumbAction.stringId,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "images.png"),
                                                                fullUpdate=False)


        # Вставка ссылок
        self._application.actionController.getAction (LINK_STR_ID).setFunc (lambda param: insertLink (self._application))

        self._application.actionController.appendMenuItem (LINK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "link.png"),
                                                                fullUpdate=False)


        # Вставка якоря
        self._application.actionController.getAction (ANCHOR_STR_ID).setFunc (lambda param: self.turnText (u"[[#", u"]]"))

        self._application.actionController.appendMenuItem (ANCHOR_STR_ID, menu)
        self._application.actionController.appendToolbarButton (ANCHOR_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "anchor.png"),
                                                                fullUpdate=False)


        # Вставка горизонтальной линии
        self._application.actionController.getAction (HORLINE_STR_ID).setFunc (lambda param: self.replaceText (u"----"))

        self._application.actionController.appendMenuItem (HORLINE_STR_ID, menu)
        self._application.actionController.appendToolbarButton (HORLINE_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "text_horizontalrule.png"),
                                                                fullUpdate=False)


        # Вставка разрыва страницы
        self._application.actionController.getAction (LINE_BREAK_STR_ID).setFunc (lambda param: self.replaceText (u"[[<<]]"))

        self._application.actionController.appendMenuItem (LINE_BREAK_STR_ID, menu)
        self._application.actionController.appendToolbarButton (LINE_BREAK_STR_ID,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "linebreak.png"),
                                                                fullUpdate=False)


        # Вставка формулы
        self._application.actionController.appendMenuItem (WikiEquationAction.stringId, menu)
        self._application.actionController.appendToolbarButton (WikiEquationAction.stringId,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "equation.png"),
                                                                fullUpdate=False)

        # Текущая дата
        self._application.actionController.getAction (CURRENT_DATE).setFunc (lambda param: insertCurrentDate (self.mainWindow,
                                                                                                              self.codeEditor))

        self._application.actionController.appendMenuItem (CURRENT_DATE, menu)
        self._application.actionController.appendToolbarButton (CURRENT_DATE,
                                                                toolbar,
                                                                os.path.join (self.imagesDir, "date.png"),
                                                                fullUpdate=False)


        self.toolsMenu.AppendSeparator()

        # Преобразовать некоторые символы в и их HTML-представление
        self._application.actionController.getAction (HTML_ESCAPE_STR_ID).setFunc (lambda param: self.escapeHtml ())
        self._application.actionController.appendMenuItem (HTML_ESCAPE_STR_ID, menu)
