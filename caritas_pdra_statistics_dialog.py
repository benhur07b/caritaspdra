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
        self.selectAllFieldsBtn.clicked.connect(self.fieldsList.selectAll)
        self.unselectAllFieldsBtn.clicked.connect(self.fieldsList.clearSelection)
        self.selectAllSummariesBtn.clicked.connect(self.summariesList.selectAll)
        self.unselectAllSummariesBtn.clicked.connect(self.summariesList.clearSelection)

        self.categories = indicators.get_list_of_categories()
        self.filterByCategoryComboBox.addItems(sorted(self.categories))

        self.init_fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldsList.addItems(self.init_fieldnames)

        self.filterByCategoryComboBox.currentIndexChanged[str].connect(self.change_category)

        self.selectHHComboBox.currentIndexChanged[str].connect(self.change_household)


    def run(self):

        household = self.selectHHComboBox.currentLayer()
        boundary = self.selectAdminComboBox.currentLayer()
        stats = self.get_summaries()
        fields = self.get_indicators_to_compute()

        parameters = {'INPUT': boundary,
                      'JOIN': household,
                      'PREDICATE' : [0],
                      'JOIN_FIELDS' : fields,
                      'SUMMARIES' : stats,
                      'DISCARD_NONMATCHING' : False,
                      'OUTPUT' : 'memory:' }

        '''If there is at least 1 stat and field selected, compute for a summary'''
        if (len(stats) > 0) and (len(fields) > 0):
            processing.runAndLoadResults("qgis:joinbylocationsummary", parameters)

        '''If only 1 stat and 1 field is selected, add symbology and label'''
        if (len(stats) == 1) and (len(fields) == 1):
            pass

        layer = QgsProject.instance().mapLayersByName("Joined layer")[0]
        layer.setName("{}_{}".format(household.name(), "SUMMARY"))


    def get_summaries(self):
        """Returns the checked stats to compute"""

        return [x.row() for x in self.summariesList.selectedIndexes()]


    def get_indicators_to_compute(self):
        """Get the field to compute statistics for"""

        return [indicators.get_indicator_code_from_name(name) for name in [field.text() for field in self.fieldsList.selectedItems()]]


    def get_pdra_indicators_in_hh_layer(self):
        """Gets the PDRA indicators present in the hh_layer"""

        household = self.selectHHComboBox.currentLayer()
        household_fields = [field.name() for field in household.fields().toList()]
        category = self.filterByCategoryComboBox.currentText()
        pdra_fields = indicators.get_dict_of_indicator_codes_per_category()[category]

        fields = list(set(household_fields).intersection(pdra_fields))
        fieldnames = [indicators.get_indicator_name_from_code(field) for field in fields]

        return sorted(fieldnames)


    def change_household(self):
        """Change the contents of the Select Field Combo Box when the household layer is changed"""

        self.fieldsList.clear()

        fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldsList.addItems(fieldnames)


    def change_category(self):
        """Change the contents of the Select Field Combo Box when the category is changed"""

        self.fieldsList.clear()

        fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldsList.addItems(fieldnames)
