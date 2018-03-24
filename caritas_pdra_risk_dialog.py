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
from .caritas_pdra_constants import *

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
        # self.setWindowTitle(self.tr('PDRA Risk Computations'))

        # Setup button responses
        self.buttonBox.accepted.connect(self.run)
        self.buttonBox.rejected.connect(self.close)
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


    def get_selected_indicator_names(self):
        """Get the indicator codes of the indicators selected for each list widget."""

        selected_haz = self.hazListWidget.selectedIndexes()
        selected_haz_names = [str(x.data()) for x in selected_haz]

        selected_vul = self.vulListWidget.selectedIndexes()
        selected_vul_names = [str(x.data()) for x in selected_vul]

        selected_cap = self.capListWidget.selectedIndexes()
        selected_cap_names = [str(x.data()) for x in selected_cap]

        selected_all_names = selected_haz_names + selected_vul_names + selected_cap_names

        return {
            "Hazard": selected_haz_names,
            "Vulnerability": selected_vul_names,
            "Capacity": selected_cap_names,
            "All": selected_all_names
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
            "Risk": count_haz + count_vul  # computation or risk is H + V - C
        }


    def run(self):

        # household = QgsProject.instance().mapLayersByName(self.selectHHComboBox.currentText())[0]
        household = self.selectHHComboBox.currentLayer()
        result_basename = self.resultBasenameLineEdit.text()

        # codes of selected indicators
        selected_indicators = self.get_selected_indicator_names()
        haz_codes = selected_indicators['Hazard']
        vul_codes = selected_indicators['Vulnerability']
        cap_codes = selected_indicators['Capacity']
        # codes of information category (household)
        info_codes = indicators.get_indicator_names_from_indicators_list(indicators.get_list_of_indicators_in_category("Information"))

        # field indices of selected indicators and information fields
        haz_indexes = [household.fields().indexFromName(code) for code in haz_codes]
        vul_indexes = [household.fields().indexFromName(code) for code in vul_codes]
        cap_indexes = [household.fields().indexFromName(code) for code in cap_codes]
        info_indexes = [household.fields().indexFromName(code) for code in info_codes]
        risk_indexes = haz_indexes + vul_indexes + cap_indexes

        cat_indexes = {'Hazard': haz_indexes,
                       'Vulnerability': vul_indexes,
                       'Capacity': cap_indexes,
                       'Risk': risk_indexes}

        haz_name = "{}_HAZARD".format(result_basename)
        vul_name = "{}_VULNERABILITY".format(result_basename)
        cap_name = "{}_CAPACITY".format(result_basename)
        risk_name = "{}_RISK".format(result_basename)

        # count for main indicators per category, the main indicator is the value after the first underscore in the field name (X_MAIN)
        cat_counts = self.count_main_indicators()
        haz_count = cat_counts['Hazard']
        vul_count = cat_counts['Vulnerability']
        cap_count = cat_counts['Capacity']
        risk_count = cat_counts['Risk']

        if len(haz_indexes) > 0:
            self.compute_category_values(household,
                                         haz_name,
                                         haz_indexes,
                                         haz_count,
                                         info_indexes,
                                         "HAZ")

        if len(vul_indexes) > 0:
            self.compute_category_values(household,
                                         vul_name,
                                         vul_indexes,
                                         vul_count,
                                         info_indexes,
                                         "VUL")

        if len(cap_indexes) > 0:
            self.compute_category_values(household,
                                         cap_name,
                                         cap_indexes,
                                         cap_count,
                                         info_indexes,
                                         "CAP")

        if (len(haz_indexes) > 0) and (len(vul_indexes) > 0) and (len(cap_indexes) > 0):
            self.compute_risk(household,
                              risk_name,
                              cat_indexes,
                              cat_counts,
                              info_indexes,
                              ["HAZ", "VUL", "CAP", "RISK"]
                              )

        if len(haz_indexes + vul_indexes + cap_indexes) == 0:
            msg = "No indicators selected. Will close dialog. Try again."
            QMessageBox.critical(self.parent, "WARNING", msg)

        self.close()


    def compute_category_values(self,
                                household,
                                name,
                                cat_indexes,
                                cat_count,
                                info_indexes,
                                cat):

        '''Create a copy of the household layer to hold output values'''
        copy_vector_layer(household, name, "Point")
        layer = QgsProject.instance().mapLayersByName(name)[0]

        res = layer.dataProvider().addAttributes([QgsField("{}_TOTAL".format(cat), QVariant.Double, 'double', 4, 2)])
        layer.updateFields()

        res = layer.dataProvider().addAttributes([QgsField("{}_NORM".format(cat), QVariant.Double, 'double', 4, 2)])
        layer.updateFields()

        res = layer.dataProvider().addAttributes([QgsField("{}_LEVEL".format(cat), QVariant.String)])
        layer.updateFields()

        total_field = layer.fields().indexFromName("{}_TOTAL".format(cat))
        norm_field = layer.fields().indexFromName("{}_NORM".format(cat))
        level_field = layer.fields().indexFromName("{}_LEVEL".format(cat))

        '''Compute for Category Total and Level'''
        features = layer.getFeatures()
        for f in features:
            layer.startEditing()
            attr = f.attributes()

            total = 0

            for index in cat_indexes:
                try:
                    value = float(indicators.get_value_from_name(layer.fields().at(index).name()))
                    total += (float(attr[index]) * value)
                except (TypeError, ValueError) as e:
                    total += 0

            cat_norm = total/cat_count

            f[total_field] = total
            f[norm_field] = cat_norm

            if cat_norm < 0.50:
                f[level_field] = "LOW"

            elif cat_norm >= 0.50 and cat_norm <= 0.75:
                f[level_field] = "MEDIUM"

            else:
                f[level_field] = "HIGH"

            layer.updateFeature(f)
        layer.commitChanges()

        '''Remove unneeded fields'''
        retain_fields(layer, info_indexes + [norm_field, total_field, level_field])

        '''Add symbology (color LOW-MEDIUM-HIGH)'''
        if cat == "CAP":
            # self.add_symbology(layer,
            #                    cat,
            #                    RISK_COLORS_INV)

            add_categorized_symbology(layer,
                                      "{}_LEVEL".format(cat),
                                      RISK_COLORS_INV)

        else:
            add_categorized_symbology(layer,
                                      "{}_LEVEL".format(cat),
                                      RISK_COLORS)


    def compute_risk(self,
                     household,
                     name,
                     cat_indexes,
                     cat_counts,
                     info_indexes,
                     cats):

        copy_vector_layer(household, name, "Point")
        layer = QgsProject.instance().mapLayersByName(name)[0]

        total_fields = {}
        norm_fields = {}
        level_fields = {}

        '''Category fields'''
        for cat in cats[:3]:
            res = layer.dataProvider().addAttributes([QgsField("{}_TOTAL".format(cat), QVariant.Double, 'double', 4, 2)])
            layer.updateFields()

            res = layer.dataProvider().addAttributes([QgsField("{}_NORM".format(cat), QVariant.Double, 'double', 4, 2)])
            layer.updateFields()

            res = layer.dataProvider().addAttributes([QgsField("{}_LEVEL".format(cat), QVariant.String)])
            layer.updateFields()

        for cat in cats[:3]:
            total_fields[cat] = layer.fields().indexFromName("{}_TOTAL".format(cat))
            norm_fields[cat] = layer.fields().indexFromName("{}_NORM".format(cat))
            level_fields[cat] = layer.fields().indexFromName("{}_LEVEL".format(cat))

        '''Risk fields'''
        res = layer.dataProvider().addAttributes([QgsField("RISK_NORM", QVariant.Double, 'double', 4, 2)])
        layer.updateFields()

        res = layer.dataProvider().addAttributes([QgsField("RISK_LEVEL", QVariant.String)])
        layer.updateFields()

        norm_field = layer.fields().indexFromName("RISK_NORM")
        level_field = layer.fields().indexFromName("RISK_LEVEL")

        '''Edit attribute table'''
        features = layer.getFeatures()
        for f in features:
            layer.startEditing()
            attr = f.attributes()

            haz_total = 0
            vul_total = 0
            cap_total = 0
            # risk_total = 0

            for index in cat_indexes["Risk"]:
                try:
                    x = float(attr[index])
                    value = float(indicators.get_value_from_name(layer.fields().at(index).name()))
                    if index in cat_indexes["Hazard"]:

                        haz_total += (x * value)
                        # risk_total += x
                    if index in cat_indexes["Vulnerability"]:
                        vul_total += (x * value)
                        # risk_total += x
                    if index in cat_indexes["Capacity"]:
                        cap_total += (x * value)
                        # risk_total -= x

                except (TypeError, ValueError) as e:
                    haz_total += 0
                    vul_total += 0
                    cap_total += 0
                    # risk_total += 0

            if cap_total == 0:  # make sure cap_total is always positive because it is a divisor
                cap_total = 1

            haz_norm = haz_total/cat_counts["Hazard"]
            vul_norm = vul_total/cat_counts["Vulnerability"]
            cap_norm = cap_total/cat_counts["Capacity"]
            risk_norm = ((haz_total + vul_total)/cap_total)/((cat_counts["Hazard"] + cat_counts["Vulnerability"]))
            # risk_level = risk_total/cat_counts["Risk"]

            f[total_fields["HAZ"]] = haz_total
            f[total_fields["VUL"]] = vul_total
            f[total_fields["CAP"]] = cap_total

            f[norm_fields["HAZ"]] = haz_norm
            f[norm_fields["VUL"]] = vul_norm
            f[norm_fields["CAP"]] = cap_norm
            f[norm_field] = risk_norm

            if haz_norm < 0.50:
                f[level_fields["HAZ"]] = "LOW"

            elif haz_norm >= 0.50 and haz_norm <= 0.75:
                f[level_fields["HAZ"]] = "MEDIUM"

            else:
                f[level_fields["HAZ"]] = "HIGH"

            if vul_norm < 0.50:
                f[level_fields["VUL"]] = "LOW"

            elif vul_norm >= 0.50 and vul_norm <= 0.75:
                f[level_fields["VUL"]] = "MEDIUM"

            else:
                f[level_fields["VUL"]] = "HIGH"

            if cap_norm < 0.50:
                f[level_fields["CAP"]] = "LOW"

            elif cap_norm >= 0.50 and cap_norm <= 0.75:
                f[level_fields["CAP"]] = "MEDIUM"

            else:
                f[level_fields["CAP"]] = "HIGH"

            if risk_norm < 0.25:
                f[level_field] = "LOW"

            elif risk_norm >= 0.25 and risk_norm <= 0.50:
                f[level_field] = "MEDIUM"

            else:
                f[level_field] = "HIGH"

            layer.updateFeature(f)
        layer.commitChanges()

        '''Remove unneeded fields'''
        retain_fields(layer,
                      info_indexes + [norm_field, level_field] + list(norm_fields.values()) + list(total_fields.values()) + list(level_fields.values()))

        add_categorized_symbology(layer,
                                  "RISK_LEVEL",
                                  RISK_COLORS)
