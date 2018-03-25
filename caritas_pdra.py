# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Caritas PDRA Analysis Tool

 This plugin performs different analysis using Caritas-Philippines
 Participatory Disaster Risk Assessment (PDRA) data.
                             -------------------
        begin                : 2018-02-15
        copyright            : (C) 2018 by Ben Hur Pintor
        email                : bhs.pintor@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/

 Contains the logic that runs the plugin
"""

__author__ = 'Ben Hur S. Pintor <bhs.pintor@gmail.com>'
__date__ = '02/15/2018'

# from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
# from PyQt5.QtGui import QIcon
# from PyQt5.QtWidgets import QAction

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qgis.core import *

# Initialize Qt resources from file resources_rc.py
from .resources_rc import *
# Import the code for the dialog
# from .caritas_pdra_risk_dialog import CaritasPDRARiskDialog
import os.path


class CaritasPDRA:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'CaritasPDRA_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        # self.dlg = CaritasPDRADialog()

        # Declare instance attributes
        self.action_caritas_pdra_risk = None
        self.action_caritas_pdra_summary = None
        self.action_caritas_pdra_summary_risk = None
        self.actions = []
        self.menu = self.tr(u'&Caritas PDRA Analysis Tool')

        # Create a dockable toolbar aside from the Menu in "Plugins"
        self.toolbar = self.iface.addToolBar(u'CaritasPDRA')
        self.toolbar.setObjectName(u'CaritasPDRA')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('CaritasPDRA', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action


    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        self.toolbar = self.iface.addToolBar('CaritasPDRA')
        self.toolbar.setObjectName('CaritasPDRAToolbar')

        # Create the Menu in plugins
        self._create_caritas_pdra_risk_action()
        self._create_caritas_pdra_summary_action()
        self._create_caritas_pdra_summary_risk_action()


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Caritas PDRA Analysis Tool'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    '''PDRA Risk Computation'''
    def _create_caritas_pdra_risk_action(self):
        """Create action for PDRA risk computations"""

        icon = ':plugins/caritas_pdra/img/icons/icon-risk.png'
        self.add_action(
            icon,
            text=self.tr(u'Compute Hazard, Vulnerability, Capacity, and Risk from PDRA Data (shp-version)'),
            status_tip=self.tr(u'Compute Hazard, Vulnerability, Capacity, and Risk from PDRA Data (shp-version)'),
            whats_this=self.tr(u'Compute Hazard, Vulnerability, Capacity, and Risk from PDRA Data (shp-version)'),
            callback=self.caritas_pdra_risk,
            parent=self.iface.mainWindow()
        )


    def caritas_pdra_risk(self):
        """Show dialog for PDRA Risk Analysis"""

        from .caritas_pdra_risk_dialog import CaritasPDRARiskDialog

        '''Run only if there are layers already loaded in QGIS'''
        if len(QgsProject.instance().mapLayers()) > 0:
            dialog = CaritasPDRARiskDialog(
                self.iface.mainWindow())
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)


    '''PDRA Summary Computation'''
    def _create_caritas_pdra_summary_action(self):
        """Create action for PDRA summary computations"""

        icon = ':plugins/caritas_pdra/img/icons/icon-summary.png'
        self.add_action(
            icon,
            text=self.tr(u'Summarize or Aggregate PDRA Data by Location (shp-vesion)'),
            status_tip=self.tr(u'Summarize or Aggregate PDRA Data by Location (shp-vesion)'),
            whats_this=self.tr(u'Summarize or Aggregate PDRA Data by Location (shp-vesion)'),
            callback=self.caritas_pdra_summary,
            parent=self.iface.mainWindow()
        )


    def caritas_pdra_summary(self):
        """Show dialog for PDRA Summary Analysis"""

        from .caritas_pdra_summary_dialog import CaritasPDRASummaryDialog

        '''Run only if there are layers already loaded in QGIS'''
        if len(QgsProject.instance().mapLayers()) > 0:
            dialog = CaritasPDRASummaryDialog(
                self.iface.mainWindow())
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)


    '''Statistics on Hazard, Vulnerability, Capacity, and Risk Computed from PDRA Data'''
    def _create_caritas_pdra_summary_risk_action(self):
        """Create action for PDRA risk summary computations"""

        icon = ':plugins/caritas_pdra/img/icons/icon-summary-risk.png'
        self.add_action(
            icon,
            text=self.tr(u'Statistics on Hazard, Vulnerability, Capacity, and Risk Computed from PDRA Data (shp-version)'),
            status_tip=self.tr(u'Statistics on Hazard, Vulnerability, Capacity, and Risk Computed from PDRA Data (shp-version)'),
            whats_this=self.tr(u'Statistics on Hazard, Vulnerability, Capacity, and Risk Computed from PDRA Data (shp-version)'),
            callback=self.caritas_pdra_summary_risk,
            parent=self.iface.mainWindow()
        )

    def caritas_pdra_summary_risk(self):
        """Show dialog for PDRA Summary Risk Analysis"""

        from .caritas_pdra_summary_risk_dialog import CaritasPDRASummaryRiskDialog

        '''Run only if there are layers already loaded in QGIS'''
        if len(QgsProject.instance().mapLayers()) > 0:
            dialog = CaritasPDRASummaryRiskDialog(
                self.iface.mainWindow())
            dialog.exec_()

        else:
            msg = "NO LAYERS FOUND.\n\nAdd layers first before running the plugin."
            QMessageBox.critical(self.iface.mainWindow(), "WARNING", msg)
