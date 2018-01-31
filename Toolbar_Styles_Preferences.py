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

"""Toolbar style for FreeCAD - Preferences."""


import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui
import Toolbar_Style_Gui as tsg

mw = Gui.getMainWindow()
p = App.ParamGet("User parameter:BaseApp/ToolbarStyle")


def dialog():
    """Toolbar style preferences dialog."""

    def onAccepted():
        """Close dialog on button close."""
        dia.done(1)

    def onFinished():
        """ Delete dialog on close."""
        dia.deleteLater()

    # Dialog
    dia = QtGui.QDialog(mw)
    dia.setModal(True)
    dia.resize(900, 500)
    dia.setWindowTitle("Toolbar style preferences")
    dia.finished.connect(onFinished)

    layout = QtGui.QVBoxLayout()
    dia.setLayout(layout)

    # Widgets
    widget = QtGui.QWidget()
    loWidget = QtGui.QVBoxLayout()
    widget.setLayout(loWidget)
    scroll = QtGui.QScrollArea()
    scroll.setWidgetResizable(True)
    scroll.setWidget(widget)
    layout.addWidget(scroll)

    # Style
    loStyle = QtGui.QVBoxLayout()
    grpBoxStyle = QtGui.QGroupBox("Style:")
    grpBoxStyle.setLayout(loStyle)
    rBtnIcon = QtGui.QRadioButton("Icon", grpBoxStyle)
    rBtnIcon.setObjectName("Icon")
    rBtnIcon.setToolTip("Buttons with icon only")
    rBtnText = QtGui.QRadioButton("Text", grpBoxStyle)
    rBtnText.setObjectName("Text")
    rBtnText.setToolTip("Buttons with text only")
    rBtnIconText = QtGui.QRadioButton("Icon and text", grpBoxStyle)
    rBtnIconText.setObjectName("IconText")
    rBtnIconText.setToolTip("Buttons with icon and text")
    rBtnTextBelow = QtGui.QRadioButton("Text below the icon", grpBoxStyle)
    rBtnTextBelow.setObjectName("TextBelow")
    rBtnTextBelow.setToolTip("Buttons with icon and text below the icon")
    loStyle.addWidget(rBtnIcon)
    loStyle.addWidget(rBtnText)
    loStyle.addWidget(rBtnIconText)
    loStyle.addWidget(rBtnTextBelow)

    btnStyle = p.GetString("Style")

    if btnStyle == "Text":
        rBtnText.setChecked(True)
    elif btnStyle == "IconText":
        rBtnIconText.setChecked(True)
    elif btnStyle == "TextBelow":
        rBtnTextBelow.setChecked(True)
    else:
        rBtnIcon.setChecked(True)

    def onGrpBoxStyle(checked):
        """Set toolbar style."""
        if checked:
            for i in grpBoxStyle.findChildren(QtGui.QRadioButton):
                if i.isChecked():
                    p.SetString("Style", i.objectName())
        tsg.onWorkbench()

    rBtnIcon.toggled.connect(onGrpBoxStyle)
    rBtnText.toggled.connect(onGrpBoxStyle)
    rBtnIconText.toggled.connect(onGrpBoxStyle)
    rBtnTextBelow.toggled.connect(onGrpBoxStyle)

    # Button close
    btnClose = QtGui.QPushButton("Close")
    btnClose.setToolTip("Close the preferences dialog")
    btnClose.clicked.connect(onAccepted)

    loBtnClose = QtGui.QHBoxLayout()
    loBtnClose.addStretch()
    loBtnClose.addWidget(btnClose)

    loWidget.addWidget(grpBoxStyle)
    loWidget.addStretch()
    layout.insertLayout(1, loBtnClose)

    btnClose.setDefault(True)
    btnClose.setFocus()

    return dia
