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

 Contains code for the PDRA Summary Risk Computations.
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
from .caritas_pdra_summary_risk_dialog_ui import Ui_CaritasPDRASummaryRiskDialog

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'caritas_pdra_risk_dialog_ui.ui'))

# import the PDRA indicators
from .caritas_pdra_utilities import *
from .caritas_pdra_constants import *

indicators_path = os.path.dirname(__file__) + '/indicators/pdra-household-indicators.csv'
indicators = Indicators(indicators_path)


class CaritasPDRASummaryRiskDialog(QDialog, Ui_CaritasPDRASummaryRiskDialog):

    def __init__(self,
                 parent=None):
        """Constructor."""
        super(CaritasPDRASummaryRiskDialog, self).__init__(parent)
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
        self.selectAllSummariesBtn.clicked.connect(self.summariesList.selectAll)
        self.unselectAllSummariesBtn.clicked.connect(self.summariesList.clearSelection)

        self.selectHHComboBox.currentIndexChanged[str].connect(self.change_household)
        self.selectBoundaryComboBox.currentIndexChanged[str].connect(self.change_boundary)

        self.change_boundary()
        self.change_household()


    def run(self):

        # pass
        household = self.selectHHComboBox.currentLayer()
        boundary = self.selectBoundaryComboBox.currentLayer()
        summaries = sorted(self.get_summaries())
        fields = self.get_indicators_to_compute()
        boundaryID = self.selectBoundaryIDFieldComboBox.currentText()
        level = self.filterByCategoryComboBox.currentText()

        try:
            assert len(summaries) > 0
            assert len(fields) > 0
            assert boundaryID != ''

            field = fields[0]

            summary_indexes = [summary[0] for summary in summaries]


            for summary in summaries:
                if summary[0] == 0:

                    outname = "{} ({} - {})".format(household.name(), field, summary[1])
                    self.total_households(household,
                                          boundary,
                                          field,
                                          fields,
                                          summary,
                                          outname)

                if summary[0] == 1:

                    outname = "{} ({} - {} [{}])".format(household.name(), field, summary[1], level)
                    self.households_at_risk(household,
                                            boundary,
                                            boundaryID,
                                            field,
                                            fields,
                                            summary,
                                            level,
                                            outname)

                if summary[0] == 2:

                    outname = "{} ({} - {} [{}])".format(household.name(), field, summary[1], level)
                    outfield = "{}_{}_PERCENTAGE".format(field, level)

                    layer_1 = ''
                    layer_2 = ''

                    hh_field = "{}_HOUSEHOLDS".format(field)
                    low_field = "{}_LOW".format(field)
                    med_field = "{}_MEDIUM".format(field)
                    high_field = "{}_HIGH".format(field)
                    perc_fields = ["{}_{}_PERCENTAGE".format(field, lvl) for lvl in ["LOW", "MEDIUM", "HIGH"]]

                    if 0 not in summary_indexes:
                        self.total_households(household,
                                              boundary,
                                              field,
                                              fields,
                                              summary,
                                              "temp_1")

                        layer_1 = QgsProject.instance().mapLayersByName("temp_1")[0]

                    else:
                        name_1 = "{} ({} - {})".format(household.name(), field, summaries[summary_indexes.index(0)][1])
                        layer_1 = QgsProject.instance().mapLayersByName(name_1)[0]

                    if 1 not in summary_indexes:
                        self.households_at_risk(household,
                                                boundary,
                                                boundaryID,
                                                field,
                                                fields,
                                                summary,
                                                level,
                                                "temp_2")

                        layer_2 = QgsProject.instance().mapLayersByName("temp_2")[0]

                    else:
                        name_2 = "{} ({} - {} [{}])".format(household.name(), field, summaries[summary_indexes.index(1)][1], level)
                        layer_2 = QgsProject.instance().mapLayersByName(name_2)[0]


                    parameters_1 = {'INPUT': layer_1,
                                    'INPUT_2': layer_2,
                                    'FIELD': boundaryID,
                                    'FIELD_2': boundaryID,
                                    'FIELDS_TO_COPY': [low_field, med_field, high_field],
                                    'OUTPUT': 'memory:',
                                    'METHOD': 1,
                                  }

                    processing.runAndLoadResults("qgis:joinattributestable", parameters_1)
                    layer = QgsProject.instance().mapLayersByName("Joined layer")[0]
                    layer.setName(outname)

                    for perc_field in perc_fields:
                        res = layer.dataProvider().addAttributes([QgsField(perc_field, QVariant.Double, 'double', 4, 2)])
                        layer.updateFields()

                    hh_index = layer.fields().indexFromName(hh_field)
                    low_index = layer.fields().indexFromName(low_field)
                    med_index = layer.fields().indexFromName(med_field)
                    high_index = layer.fields().indexFromName(high_field)
                    low_perc_index = layer.fields().indexFromName(perc_fields[0])
                    med_perc_index = layer.fields().indexFromName(perc_fields[1])
                    high_perc_index = layer.fields().indexFromName(perc_fields[2])

                    features = layer.getFeatures()

                    for f in features:
                        layer.startEditing()
                        attr = f.attributes()

                        try:
                            f[low_perc_index] = 100*float(attr[low_index])/float(attr[hh_index])
                        except (TypeError, ValueError) as e:
                            pass

                        try:
                            f[med_perc_index] = 100*float(attr[med_index])/float(attr[hh_index])
                        except (TypeError, ValueError) as e:
                            pass

                        try:
                            f[high_perc_index] = 100*float(attr[high_index])/float(attr[hh_index])
                        except (TypeError, ValueError) as e:
                            pass

                        layer.updateFeature(f)
                    layer.commitChanges()

                    if 0 not in summary_indexes:
                        QgsProject.instance().removeMapLayers([layer_1.id()])

                    if 1 not in summary_indexes:
                        QgsProject.instance().removeMapLayers([layer_2.id()])

                    add_ranged_symbology(layer,
                                         'IF("{outfield}" IS NULL, 0, "{outfield}")'.format(outfield=outfield),
                                         PERCENTAGE_COLORS)
                    add_labels(layer,
                               'IF("{outfield}" IS NULL, {zero}, concat(format_number(to_string("{outfield}"), 0), {percent}))'.format(outfield=outfield, zero=str("'0%'"), percent=str("'%'")))

        except AssertionError:
            msg = "Must select an indicator and a summary to be computed. Will close dialog. Try again."
            QMessageBox.critical(self.parent, "WARNING", msg)

        self.close()


    def get_summaries(self):
        """Returns the checked stats to compute"""

        # return [[x.row(), x.text()] for x in self.summariesList.selectedIndexes()]   # return index number of selected summaries
        rows = [x.row() for x in self.summariesList.selectedIndexes()]
        names = [x.text() for x in self.summariesList.selectedItems()]

        return[[rows[x], names[x]] for x in range(len(rows))]


    def get_indicators_to_compute(self):
        """Get the field to compute statistics for"""

        return [field.text() for field in self.fieldsList.selectedItems()]
        # return [indicators.get_indicator_code_from_name(name) for name in [field.text() for field in self.fieldsList.selectedItems()]]


    def get_pdra_indicators_in_hh_layer(self):
        """Gets the PDRA indicators present in the hh_layer"""

        household = self.selectHHComboBox.currentLayer()
        household_fields = [field.name() for field in household.fields().toList()]
        # category = self.filterByCategoryComboBox.currentText()
        pdra_fields = indicators.get_dict_of_indicator_names_per_category()["Risk"]
        # pdra_fields = indicators.get_dict_of_indicator_codes_per_category()[category]

        fields = list(set(household_fields).intersection(pdra_fields))
        # fieldnames = [indicators.get_indicator_name_from_code(field) for field in fields]
        fieldnames = fields

        return sorted(fieldnames)


    def change_household(self):
        """Change the contents of the Select Field Combo Box when the household layer is changed"""

        self.fieldsList.clear()

        fieldnames = sorted(self.get_pdra_indicators_in_hh_layer())
        self.fieldsList.addItems(fieldnames)


    def change_boundary(self):
        """Change the contents of the boundaryID Combo Box when the boundary layer is changed"""

        self.selectBoundaryIDFieldComboBox.setLayer(self.selectBoundaryComboBox.currentLayer())


    def total_households(self,
                         household,
                         boundary,
                         field,
                         fields,
                         summary,
                         outname):

        '''
        Number of households
        Perform join attributes by location (summary) [count]
        '''
        outfield = "{field}_HOUSEHOLDS".format(field=field)
        field_expression = 'IF("{outfield}" IS NULL, 0, "{outfield}")'.format(outfield=outfield)
        parameters = {'INPUT': boundary,
                      'JOIN': household,
                      'PREDICATE': [0],
                      'JOIN_FIELDS': fields,
                      'SUMMARIES': [0],
                      'DISCARD_NONMATCHING': False,
                      'OUTPUT': 'memory:'}

        processing.runAndLoadResults("qgis:joinbylocationsummary", parameters)
        layer_1 = QgsProject.instance().mapLayersByName("Joined layer")[0]
        refactor_fields(layer_1, [["{}_count".format(field), outfield]])
        QgsProject.instance().removeMapLayers([layer_1.id()])
        layer = QgsProject.instance().mapLayersByName("Refactored")[0]
        layer.setName(outname)

        # self.add_symbology(layer, outfield)
        add_ranged_symbology(layer,
                             field_expression,
                             COUNT_HH_COLORS)
        add_labels(layer,
                   field_expression)


    def households_at_risk(self,
                           household,
                           boundary,
                           boundaryID,
                           field,
                           fields,
                           summary,
                           level,
                           outname):

        '''
        Number of households at risk
        Filter households where indicator > 0
        Perform join attributes by location (summary) [count] on filtered layer
        '''

        outfield = "{field}_{level}".format(field=field, level=level)
        field_expression = 'IF("{outfield}" IS NULL, 0, "{outfield}")'.format(outfield=outfield)
        levels = ['LOW', 'MEDIUM', 'HIGH']
        for lvl in levels:
            household.setSubsetString(u'"{}" = {}'.format(field, "'{}'".format(lvl)))
            parameters = {'INPUT': boundary,
                          'JOIN': household,
                          'PREDICATE': [0],
                          'JOIN_FIELDS': fields,
                          'SUMMARIES': [0],
                          'DISCARD_NONMATCHING': False,
                          'OUTPUT': 'memory:'}

            processing.runAndLoadResults("qgis:joinbylocationsummary", parameters)
            layer = QgsProject.instance().mapLayersByName("Joined layer")[0]
            layer.setName("{}".format(lvl))

        household.setSubsetString(u"")

        layers = [QgsProject.instance().mapLayersByName(lvl)[0] for lvl in levels]

        parameters_1 = {'INPUT': layers[0],
                        'INPUT_2': layers[1],
                        'FIELD': boundaryID,
                        'FIELD_2': boundaryID,
                        'FIELDS_TO_COPY': ["{}_count".format(field)],
                        'OUTPUT': 'memory:',
                        'METHOD': 1,
                      }

        processing.runAndLoadResults("qgis:joinattributestable", parameters_1)
        layer_1 = QgsProject.instance().mapLayersByName("Joined layer")[0]
        layer_1.setName("1")

        parameters_2 = {'INPUT': layer_1,
                        'INPUT_2': layers[2],
                        'FIELD': boundaryID,
                        'FIELD_2': boundaryID,
                        'FIELDS_TO_COPY': ["{}_count".format(field)],
                        'OUTPUT': 'memory:',
                        'METHOD': 1,
                      }

        processing.runAndLoadResults("qgis:joinattributestable", parameters_2)
        layer_2 = QgsProject.instance().mapLayersByName("Joined layer")[0]
        layer_2.setName("2")

        refactor_fields(layer_2, [["{}_count".format(field), "{}_LOW".format(field)], ["{}_count_2".format(field), "{}_MEDIUM".format(field)], ["{}_count_3".format(field), "{}_HIGH".format(field)]])
        layer = QgsProject.instance().mapLayersByName("Refactored")[0]
        layer.setName(outname)

        # self.add_symbology(layer, outfield)
        add_ranged_symbology(layer,
                             field_expression,
                             COUNT_HH_COLORS)
        add_labels(layer,
                   field_expression)

        QgsProject.instance().removeMapLayers([layer.id() for layer in layers] + [layer_1.id(), layer_2.id()])
