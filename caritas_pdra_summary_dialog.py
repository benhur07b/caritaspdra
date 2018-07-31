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

 Contains code for the PDRA Summary Computations.
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
from .caritas_pdra_summary_dialog_ui import Ui_CaritasPDRASummaryDialog

# FORM_CLASS, _ = uic.loadUiType(os.path.join(
#     os.path.dirname(__file__), 'caritas_pdra_risk_dialog_ui.ui'))

# import the PDRA indicators
from .caritas_pdra_utilities import *
from .caritas_pdra_constants import *

indicators_path = os.path.dirname(__file__) + '/indicators/pdra-household-indicators.csv'
indicators = Indicators(indicators_path)


class CaritasPDRASummaryDialog(QDialog, Ui_CaritasPDRASummaryDialog):

    def __init__(self,
                 parent=None):
        """Constructor."""
        super(CaritasPDRASummaryDialog, self).__init__(parent)
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

        self.categories = [i for i in indicators.get_list_of_categories() if i.capitalize() not in ['Information', 'Risk']]  # Only include indicators and not computed Hazard, Vulnerability, Capacity, and Risk levels
        self.filterByCategoryComboBox.addItems(sorted(self.categories))

        self.init_fieldnames = self.get_pdra_indicators_in_hh_layer()
        self.fieldsList.addItems(self.init_fieldnames)

        self.selectHHComboBox.currentIndexChanged[str].connect(self.change_household)
        self.selectBoundaryComboBox.currentIndexChanged[str].connect(self.change_boundary)
        self.filterByCategoryComboBox.currentIndexChanged[str].connect(self.change_category)

        self.change_boundary()


    def run(self):

        household = self.selectHHComboBox.currentLayer()
        boundary = self.selectBoundaryComboBox.currentLayer()
        summaries = sorted(self.get_summaries())
        fields = self.get_indicators_to_compute()
        boundaryID = self.selectBoundaryIDFieldComboBox.currentText()

        try:
            assert len(summaries) > 0
            assert len(fields) > 0
            assert boundaryID != ''

            field = fields[0]

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
                    '''
                    Number of households where indicator is present
                    Filter households where indicator > 0
                    Perform join attributes by location (summary) [count] on filtered layer
                    '''

                    outfield = "{field}_HOUSEHOLDS_WITH_INDICATOR".format(field=field)
                    field_expression = 'IF("{outfield}" IS NULL, 0, "{outfield}")'.format(outfield=outfield)
                    household.setSubsetString(u"{} > 0".format(field))

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
                    layer.setName("{} ({} - {})".format(household.name(), field, summary[1]))

                    add_ranged_symbology(layer,
                                         field_expression,
                                         COUNT_HH_COLORS)
                    add_labels(layer,
                               field_expression)

                    household.setSubsetString(u"")


                if summary[0] == 2:
                    '''
                    Percentage of Households where indicator is present
                    Perform join attributes by location (summary) [count]
                    '''
                    # Get number of households
                    parameters_1 = {'INPUT': boundary,
                                    'JOIN': household,
                                    'PREDICATE': [0],
                                    'JOIN_FIELDS': fields,
                                    'SUMMARIES': [0],
                                    'DISCARD_NONMATCHING': False,
                                    'OUTPUT': 'memory:'}

                    processing.runAndLoadResults("qgis:joinbylocationsummary", parameters_1)
                    layer_1 = QgsProject.instance().mapLayersByName("Joined layer")[0]
                    layer_1.setName("1")

                    # Get number of households with indicator
                    household.setSubsetString(u"{} > 0".format(field))

                    parameters_2 = {'INPUT': boundary,
                                    'JOIN': household,
                                    'PREDICATE': [0],
                                    'JOIN_FIELDS': fields,
                                    'SUMMARIES': [0],
                                    'DISCARD_NONMATCHING': False,
                                    'OUTPUT': 'memory:'}

                    processing.runAndLoadResults("qgis:joinbylocationsummary", parameters_2)
                    layer_2 = QgsProject.instance().mapLayersByName("Joined layer")[0]
                    layer_2.setName("2")

                    household.setSubsetString(u"")

                    # Get percentage
                    parameters = {'INPUT': layer_1,
                                  'INPUT_2': layer_2,
                                  'FIELD': boundaryID,
                                  'FIELD_2': boundaryID,
                                  'FIELDS_TO_COPY': ["{}_count".format(field)],
                                  'OUTPUT': 'memory:',
                                  'METHOD': 1,
                                  }

                    processing.runAndLoadResults("qgis:joinattributestable", parameters)
                    layer_3 = QgsProject.instance().mapLayersByName("Joined layer")[0]

                    # Remove temp layers
                    QgsProject.instance().removeMapLayers([layer_1.id(), layer_2.id()])

                    i_count = "{}_count".format(field)
                    i_count_2 = "{}_count_2".format(field)
                    i_percent = "{}_PERCENTAGE".format(field)

                    res = layer_3.dataProvider().addAttributes([QgsField(i_percent, QVariant.Double, 'double', 4, 2)])
                    layer_3.updateFields()

                    i_count_index = layer_3.fields().indexFromName(i_count)
                    i_count_2_index = layer_3.fields().indexFromName(i_count_2)
                    i_percent_index = layer_3.fields().indexFromName(i_percent)

                    # Compute percentage
                    features = layer_3.getFeatures()
                    for f in features:
                        layer_3.startEditing()
                        attr = f.attributes()

                        try:
                            f[i_percent_index] = 100*float(attr[i_count_2_index])/float(attr[i_count_index])
                        except (TypeError, ValueError) as e:
                            pass

                        layer_3.updateFeature(f)
                    layer_3.commitChanges()

                    refactor_fields(layer_3, [[i_count, "{}_HOUSEHOLDS".format(field)], [i_count_2, "{}_HOUSEHOLDS_WITH_INDICATOR".format(field)]])
                    layer = QgsProject.instance().mapLayersByName("Refactored")[0]
                    layer.setName("{} ({} - {})".format(household.name(), field, summary[1]))

                    QgsProject.instance().removeMapLayers([layer_3.id()])

                    add_ranged_symbology(layer,
                                         'IF("{}" IS NULL, 0, "{}")'.format(i_percent, i_percent),
                                         PERCENTAGE_COLORS)
                    add_labels(layer,
                               'IF("{i_percent}" IS NULL, {zero}, concat(format_number(to_string("{i_percent}"), 0), {percent}))'.format(i_percent=i_percent, zero=str("'0%'"), percent=str("'%'")))


                if summary[0] == 3:
                    '''
                    Number of Persons with Indicator Present
                    Perform join attributes by location (summary) [sum]
                    '''

                    mem_field = "_MEM_"
                    mem_fields = [f.name() for f in household.fields().toList() if mem_field in f.name()]

                    household.setSubsetString(u'"{}" > 0'.format(field))

                    # outfield = "{field}_PERSONS_WITH_INDICATOR".format(field=field)
                    outfield = "{m}_PERSONS_WITH_INDICATOR".format(m=mem_fields[len(mem_fields)-1])
                    field_expression = 'IF("{outfield}" IS NULL, 0, "{outfield}")'.format(outfield=outfield)
                    parameters = {'INPUT': boundary,
                                  'JOIN': household,
                                  'PREDICATE': [0],
                                  'JOIN_FIELDS': mem_fields,
                                  'SUMMARIES': [5],
                                  'DISCARD_NONMATCHING': False,
                                  'OUTPUT': 'memory:'}

                    processing.runAndLoadResults("qgis:joinbylocationsummary", parameters)
                    layer_1 = QgsProject.instance().mapLayersByName("Joined layer")[0]
                    refactor_fields(layer_1, [["{}_sum".format(m), "{}_PERSONS_WITH_INDICATOR".format(m)] for m in mem_fields])
                    # refactor_fields(layer_1, [["{}_sum".format(field), outfield]])
                    QgsProject.instance().removeMapLayers([layer_1.id()])

                    layer = QgsProject.instance().mapLayersByName("Refactored")[0]
                    layer.setName("{} ({} - {})".format(household.name(), field, summary[1]))

                    household.setSubsetString(u'')

                    add_ranged_symbology(layer,
                                         field_expression,
                                         COUNT_PP_COLORS)
                    add_labels(layer,
                               field_expression)

        except AssertionError:
            msg = "Must select an indicator and a summary to be computed. Will close dialog. Try again."
            QMessageBox.critical(self.parent, "WARNING", msg)

        self.close()


    def get_summaries(self):
        """Returns the checked stats to compute"""

        rows = [x.row() for x in self.summariesList.selectedIndexes()]
        names = [x.text() for x in self.summariesList.selectedItems()]

        return[[rows[x], names[x]] for x in range(len(rows))]

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


    def change_boundary(self):
        """Change the contents of the boundaryID Combo Box when the boundary layer is changed"""

        self.selectBoundaryIDFieldComboBox.setLayer(self.selectBoundaryComboBox.currentLayer())


    def change_category(self):
        """Change the contents of the Select Field Combo Box when the category is changed"""

        self.fieldsList.clear()

        fieldnames = self.get_pdra_indicators_in_hh_layer()

        self.fieldsList.addItems(fieldnames)


    def set_null_to_zero(self,
                         layer,
                         fieldName):

        field = layer.fields().indexFromName(fieldName)
        features = layer.getFeatures()
        for f in features:
            layer.startEditing()
            attr = f.attributes()

            try:
                x = float(f[field])
            except (TypeError, ValueError) as e:
                f[field] = 0

            layer.updateFeature(f)
        layer.commitChanges()


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

        add_ranged_symbology(layer,
                             field_expression,
                             COUNT_HH_COLORS)
        add_labels(layer,
                   field_expression)
