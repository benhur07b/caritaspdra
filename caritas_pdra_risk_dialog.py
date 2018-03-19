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

    def __init__(self,
                 parent=None):
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
        """Get the indicator codes of the indicators selected for each list widget."""

        selected_haz = self.hazListWidget.selectedIndexes()
        selected_haz_names = [str(x.data()) for x in selected_haz]
        selected_haz_codes = [indicators.get_indicator_code_from_name(name) for name in selected_haz_names]

        selected_vul = self.vulListWidget.selectedIndexes()
        selected_vul_names = [str(x.data()) for x in selected_vul]
        selected_vul_codes = [indicators.get_indicator_code_from_name(name) for name in selected_vul_names]

        selected_cap = self.capListWidget.selectedIndexes()
        selected_cap_names = [str(x.data()) for x in selected_cap]
        selected_cap_codes = [indicators.get_indicator_code_from_name(name) for name in selected_cap_names]

        selected_all_codes = selected_haz_codes + selected_vul_codes + selected_cap_codes

        return {
            "Hazard": selected_haz_codes,
            "Vulnerability": selected_vul_codes,
            "Capacity": selected_cap_codes,
            "All": selected_all_codes
        }


    def count_main_indicators(self):
        """Count the main indicator classifications per category among the selected indicators.

        The Format of the INDICATOR_CODE is: CATEGORY_MAINCLASS_SECONDARYCLASS_SUBCLASS
        """

        selected_indicators = self.get_selected_indicator_codes()
        count_haz = len(set(["_".join(i.split("_")[:2]) for i in selected_indicators["Hazard"]]))
        count_vul = len(set(["_".join(i.split("_")[:2]) for i in selected_indicators["Vulnerability"]]))
        count_cap = len(set(["_".join(i.split("_")[:2]) for i in selected_indicators["Hazard"]]))

        return {
            "Hazard": count_haz,
            "Vulnerability": count_vul,
            "Capacity": count_cap,
            "Risk": count_haz + count_vul - count_cap  # computation or risk is H + V - C
        }


    def run(self):

        household = QgsProject.instance().mapLayersByName(self.selectHHComboBox.currentText())[0]
        result_basename = self.resultBasenameLineEdit.text()

        # codes of selected indicators
        selected_indicators = self.get_selected_indicator_codes()
        haz_codes = selected_indicators['Hazard']
        vul_codes = selected_indicators['Vulnerability']
        cap_codes = selected_indicators['Capacity']
        # codes of information category (household)
        info_codes = indicators.get_indicator_codes_from_indicators_list(indicators.get_list_of_indicators_in_category("Information"))

        # field indices of selected indicators and information fields
        haz_indexes = [household.fields().indexFromName(code) for code in haz_codes]
        vul_indexes = [household.fields().indexFromName(code) for code in vul_codes]
        cap_indexes = [household.fields().indexFromName(code) for code in cap_codes]
        info_indexes = [household.fields().indexFromName(code) for code in info_codes]
        risk_indexes = haz_indexes + vul_indexes + cap_indexes

        haz_name = "{}_HAZARD".format(result_basename)
        vul_name = "{}_VULNERABILITY".format(result_basename)
        cap_name = "{}_CAPACITY".format(result_basename)
        risk_name = "{}_RISK".format(result_basename)

        # count for main indicators per category, the main indicator is the value after the first underscore in the field name (X_MAIN)
        main_indicator_counts = self.count_main_indicators()
        haz_count = main_indicator_counts['Hazard']
        vul_count = main_indicator_counts['Vulnerability']
        cap_count = main_indicator_counts['Capacity']
        risk_count = main_indicator_counts['Risk']

        if len(haz_indexes) > 0:
            self.compute_category_values(household,
                                         haz_name,
                                         haz_indexes,
                                         haz_count,
                                         haz_codes,
                                         info_indexes,
                                         "HAZ")

        if len(vul_indexes) > 0:
            self.compute_category_values(household,
                                         vul_name,
                                         vul_indexes,
                                         vul_count,
                                         vul_codes,
                                         info_indexes,
                                         "VUL")

        if len(cap_indexes) > 0:
            self.compute_category_values(household,
                                         cap_name,
                                         cap_indexes,
                                         cap_count,
                                         cap_codes,
                                         info_indexes,
                                         "CAP")


    def compute_category_values(self,
                                household,
                                name,
                                cat_indexes,
                                cat_count,
                                cat_codes,
                                info_indexes,
                                cat):

        '''Create a copy of the household layer to hold output values'''
        copy_vector_layer(household, name, "Point")
        layer = QgsProject.instance().mapLayersByName(name)[0]

        res = layer.dataProvider().addAttributes([QgsField("{}_TOTAL".format(cat), QVariant.Double, 'double', 4, 2)])
        layer.updateFields()

        res = layer.dataProvider().addAttributes([QgsField("{}_LEVEL".format(cat), QVariant.String)])
        layer.updateFields()

        total_field = layer.fields().indexFromName("{}_TOTAL".format(cat))
        level_field = layer.fields().indexFromName("{}_LEVEL".format(cat))

        '''Compute for Category Total and Level'''
        features = layer.getFeatures()
        for f in features:
            layer.startEditing()
            attr = f.attributes()

            total = 0

            for index in cat_indexes:
                try:
                    total += float(attr[index])
                except (TypeError, ValueError) as e:
                    total += 0

            f[total_field] = total/cat_count

            level = total/cat_count
            if level < 0.50:
                f[level_field] = "LOW"

            elif level >= 0.50 and level <= 0.75:
                f[level_field] = "MEDIUM"

            else:
                f[level_field] = "HIGH"


            layer.updateFeature(f)
        layer.commitChanges()

        '''Remove unneeded fields'''
        retain_fields(layer, info_indexes + [total_field, level_field])

        '''Add symbology (color LOW-MEDIUM-HIGH)'''
        levels = [("LOW", "yellow", "LOW"),
                  ("MEDIUM", "green", "MEDIUM"),
                  ("HIGH", "red", "HIGH")]

        categories = []

        for level, color, label in levels:
            sym = QgsSymbol.defaultSymbol(layer.geometryType())
            sym.setColor(QColor(color))
            category = QgsRendererCategory(level, sym, label)
            categories.append(category)

        renderer = QgsCategorizedSymbolRenderer("{}_LEVEL".format(cat), categories)
        layer.setRenderer(renderer)
        layer.triggerRepaint()
