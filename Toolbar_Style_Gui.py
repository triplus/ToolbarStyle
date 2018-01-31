# Toolbar style for FreeCAD (based on command panel)
# Copyright (C) 2018 triplus @ FreeCAD
#
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA

"""Toolbar style for FreeCAD - Gui."""


from PySide import QtGui
from PySide import QtCore
import FreeCADGui as Gui
import FreeCAD as App
import Toolbar_Styles_Preferences as tsp

mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/ToolbarStyle")


def accessoriesMenu():
    """Add toolbar style preferences to accessories menu."""
    pref = QtGui.QAction(mw)
    pref.setText("Toolbar style")
    pref.setObjectName("ToolbarStyle")
    pref.triggered.connect(onPreferences)
    try:
        import AccessoriesMenu
        AccessoriesMenu.addItem("ToolbarStyle")
    except ImportError:
        a = mw.findChild(QtGui.QAction, "AccessoriesMenu")
        if a:
            a.menu().addAction(pref)
        else:
            mb = mw.menuBar()
            action = QtGui.QAction(mw)
            action.setObjectName("AccessoriesMenu")
            action.setIconText("Accessories")
            menu = QtGui.QMenu()
            action.setMenu(menu)
            menu.addAction(pref)

            def addMenu():
                """Add accessories menu to the menu bar."""
                toolsMenu = mb.findChild(QtGui.QMenu, "&Tools")
                if toolsMenu:
                    toolsMenu.addAction(action)

            addMenu()
            mw.workbenchActivated.connect(addMenu)


def onPreferences():
    """Open the preferences dialog."""
    dialog = tsp.dialog()
    dialog.show()


def onWorkbench():
    """Set toolbar style on workbench activation."""
    style = p.GetString("Style")
    if style == "Text":
        mode = QtCore.Qt.ToolButtonTextOnly
    elif style == "IconText":
        mode = QtCore.Qt.ToolButtonTextBesideIcon
    elif style == "TextBelow":
        mode = QtCore.Qt.ToolButtonTextUnderIcon
    else:
        mode = QtCore.Qt.ToolButtonIconOnly

    for t in mw.findChildren(QtGui.QToolBar):
        t.setToolButtonStyle(mode)


def onStart():
    """Start toolbar style."""
    start = False
    try:
        mw.workbenchActivated
        start = True
    except AttributeError:
        pass
    if start:
        t.stop()
        t.deleteLater()
        onWorkbench()
        accessoriesMenu()
        mw.workbenchActivated.connect(onWorkbench)


t = QtCore.QTimer()
t.timeout.connect(onStart)
t.start(500)
