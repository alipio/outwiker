#!/usr/bin/python
# -*- coding: UTF-8 -*-


from outwiker.gui.baseaction import BaseAction

class DebugAction (BaseAction):
    """
    Класс действия, предназначенный для отладки действий с помощью плагина TestDebug
    """
    @property
    def title (self):
        return u"DebugAction"
    

    @property
    def strid (self):
        return u"plugin_debug_action"
    
    
    def run (self):
        print u"DebugAction.run()"
