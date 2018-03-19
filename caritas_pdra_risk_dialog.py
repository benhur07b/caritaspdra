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

 Contains code for the PDRA Risk Computations.
"""

__author__ = 'Ben Hur S. Pintor <bhs.pintor@gmail.com>'
__date__ = '02/15/2018'

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from qgis.core import *

import os

# from .resources_rc import *
from .caritas_pdra_risk_dialog_ui import Ui_CaritasPDRARiskDialog

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'caritas_pdra_risk_dialog_ui.ui'))

# import the PDRA indicators
from .caritas_pdra_utilities import *

indicators_path = os.path.dirname(__file__) + '/indicators/pdra-household-indicators.csv'
indicators = Indicators(indicators_path)


class CaritasPDRARiskDialog(QDialog, Ui_CaritasPDRARiskDialog):

    def __init__(self, parent=None):
        """Constructor."""
        super(CaritasPDRARiskDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.parent = parent
        self.setupUi(self)
        self.setWindowTitle(self.tr('PDRA Risk Computations'))

        # Setup button responses
        self.buttonBox.accepted.connect(self.run)
        self.hazSelectAllBtn.clicked.connect(self.hazListWidget.selectAll)
        self.hazUnselectAllBtn.clicked.connect(self.hazListWidget.clearSelection)
        self.vulSelectAllBtn.clicked.connect(self.vulListWidget.selectAll)
        self.vulUnselectAllBtn.clicked.connect(self.vulListWidget.clearSelection)
        self.capSelectAllBtn.clicked.connect(self.capListWidget.selectAll)
        self.capUnselectAllBtn.clicked.connect(self.capListWidget.clearSelection)

        # Populate the indicator widgets
        self.catsListWidgets = [self.capListWidget, self.vulListWidget, self.capListWidget]
        self.indicator_names_per_category = indicators.get_dict_of_indicator_names_per_category()
        self.hazListWidget.addItems(sorted(self.indicator_names_per_category['Hazard']))
        self.vulListWidget.addItems(sorted(self.indicator_names_per_category['Vulnerability']))
        self.capListWidget.addItems(sorted(self.indicator_names_per_category['Capacity']))


    def get_selected_indicator_codes(self):

        selected_haz = self.hazListWidget.selectedIndexes()
        selected_haz_names = [str(x.data()) for x in selected_exp]
        selected_haz_codes = [indicators.get_indicator_code_from_name(name) for name in selected_haz_names]

        selected_vul = self.vulListWidget.selectedIndexes()
        selected_vul_names = [str(x.data()) for x in selected_exp]
        selected_vul_codes = [indicators.get_indicator_code_from_name(name) for name in selected_vul_names]

        selected_cap = self.capListWidget.selectedIndexes()
        selected_cap_names = [str(x.data()) for x in selected_exp]
        selected_cap_codes = [indicators.get_indicator_code_from_name(name) for name in selected_cap_names]

        selected_all_codes = selected_haz_codes + selected_vul_codes + selected_cap_codes

        return {
            "Hazard": selected_haz_codes,
            "Vulnerability": selected_vul_codes,
            "Capacity": selected_cap_codes,
            "All": selected_all_codes
        }


    def count_main_indicators(self):

        selected_indicators = self.get_selected_indicator_codes()
        count_haz = len(set(["_".join(i.split("_")[:2]) for i in selected_indicators["Hazard"]]))
        count_vul = len(set(["_".join(i.split("_")[:2]) for i in selected_indicators["Vulnerability"]]))
        count_cap = len(set(["_".join(i.split("_")[:2]) for i in selected_indicators["Hazard"]]))

        return {
            "Hazard": count_haz,
            "Vulnerability": count_vul,
            "Capacity": count_cap,
            "All": count_haz + count_vul - count_cap  # computation or risk is H + V - C
        }


    def run(self):
        pass


    def compute_risk(self):
        pass
