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

import processing

import os

# from .resources_rc import *
from .caritas_pdra_statistics_dialog_ui import Ui_CaritasPDRAStatisticsDialog

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'caritas_pdra_risk_dialog_ui.ui'))

# import the PDRA indicators
from .caritas_pdra_utilities import *

indicators_path = os.path.dirname(__file__) + '/indicators/pdra-household-indicators.csv'
indicators = Indicators(indicators_path)


class CaritasPDRAStatisticsDialog(QDialog, Ui_CaritasPDRAStatisticsDialog):

    def __init__(self,
                 parent=None):
        """Constructor."""
        super(CaritasPDRAStatisticsDialog, self).__init__(parent)
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.parent = parent
        self.setupUi(self)
        # self.setWindowTitle(self.tr('PDRA Summary'))

        # Setup button responses
        self.buttonBox.accepted.connect(self.run)
        self.buttonBox.rejected.connect(self.close)
        self.selectAllBtn.clicked.connect(self.select_all_statchk)
        self.clearBtn.clicked.connect(self.clear_statchk)

        # Checkboxes
        self.checkboxes = [self.countChk,
                           self.uniqueChk,
                           self.minChk,
                           self.maxChk,
                           self.sumChk,
                           self.meanChk,
                           self.medianChk,
                           self.stdevChk]

        self.categories = indicators.get_list_of_categories()
        self.filterByCategoryComboBox.addItems(sorted(self.categories))

        self.init_fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldsList.addItems(self.init_fieldnames)

        self.filterByCategoryComboBox.currentIndexChanged[str].connect(self.change_category)

        self.selectHHComboBox.currentIndexChanged[str].connect(self.change_household)


    def run(self):

        pass

        household = self.selectHHComboBox.currentLayer()
        boundary = self.selectAdminComboBox.currentLayer()
        stats = self.get_stats()
        fields = self.get_indicator_to_compute()

        parameters = {'INPUT': boundary,
                      'JOIN': household,
                      'PREDICATE' : [0],
                      'JOIN_FIELDS' : fields,
                      'SUMMARIES' : stats,
                      'DISCARD_NONMATCHING' : False,
                      'OUTPUT' : 'memory:' }

        if len(stats) > 0:
            stats_str = ",".join(stats)

            processing.run("qgis:joinattributesbylocationsummary", parameters)



    def get_stats(self):
        """Returns the checked stats to compute"""

        pass



    def get_pdra_indicators_in_hh_layer(self):
        """Gets the PDRA indicators present in the hh_layer"""

        household = self.selectHHComboBox.currentLayer()
        household_fields = [field.name() for field in household.fields().toList()]
        category = self.filterByCategoryComboBox.currentText()
        pdra_fields = indicators.get_dict_of_indicator_codes_per_category()[category]

        fields = list(set(household_fields).intersection(pdra_fields))
        fieldnames = [indicators.get_indicator_name_from_code(field) for field in fields]

        return sorted(fieldnames)


    def get_indicator_to_compute(self):
        """Get the field to compute statistics for"""

        return [indicators.get_indicator_code_from_name(self.fieldList.currentText())]


    def change_household(self):
        """Change the contents of the Select Field Combo Box when the household layer is changed"""

        self.fieldList.clear()

        fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldList.addItems(fieldnames)


    def change_category(self):
        """Change the contents of the Select Field Combo Box when the category is changed"""

        self.fieldList.clear()

        fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldList.addItems(fieldnames)
