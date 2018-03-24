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

 Contains utility functions.
"""

__author__ = 'Ben Hur S. Pintor <bhs.pintor@gmail.com>'
__date__ = '02/15/2018'

from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import uic
from qgis.core import *
import processing

import os
import csv
import re


class Indicators():
    """Class for the PDRA Indicators.

    The Format of Household PDRA Indicators CSV is:
    index   value
    0       INDICATOR_CODE
    1       INDICATOR_NAME
    2       CATEGORY
    3       RISK_VALUE

    The Format of the INDICATOR_CODE is: CATEGORY_MAINCLASS_SECONDARYCLASS_SUBCLASS
    """

    def __init__(self,
                 indicators_path):

        self.indicators_path = indicators_path
        self.indicators_list = self.get_indicators_list()


    def get_indicators_list(self):
        """Reads the indicators CSV provided by the indicators path and saves
        it to a list.
        """

        with open(self.indicators_path, 'r') as f:
            reader = csv.reader(f)
            return list(reader)[1:]  # exclude headers


    def get_indicator_codes(self):

        return [i[0] for i in self.indicators_list]


    def get_indicator_codes_from_indicators_list(self,
                                                 indicators_list):

        return [i[0] for i in indicators_list]


    def get_indicator_names(self):

        return [i[1] for i in self.indicators_list]


    def get_indicator_names_from_indicators_list(self,
                                                 indicators_list):

        return [i[1] for i in indicators_list]


    def get_indicator_name_from_code(self,
                                     indicator_code):
        """Returns the INDICATOR_NAME of the given INDICATOR_CODE"""

        if indicator_code in self.get_indicator_codes():  # if indicator_code exists, return the indicator_name
            return [i[1] for i in self.indicators_list if i[0] == indicator_code][0]
        else:
            return None


    def get_indicator_code_from_name(self,
                                     indicator_name):
        """Returns the INDICATOR_CODE of the given INDICATOR_NAME"""

        if indicator_name in self.get_indicator_names():  # if indicator_name exists, return the indicator_code
            return [i[0] for i in self.indicators_list if i[1] == indicator_name][0]
        else:
            return None


    def get_value_from_code(self,
                            indicator_code):
        """Returns the value of the indicator using the indicator code"""

        if indicator_code in self.get_indicator_codes():  # if indicator_code exists, return the indicator_name
            return [i[3] for i in self.indicators_list if i[0] == indicator_code][0]
        else:
            return None


    def get_value_from_name(self,
                            indicator_name):
        """Returns the value of the indicator using the indicator name"""

        if indicator_name in self.get_indicator_names():  # if indicator_code exists, return the indicator_name
            return [i[3] for i in self.indicators_list if i[1] == indicator_name][0]
        else:
            return None


    def get_list_of_categories(self):
        """Returns the list of categories"""

        return sorted(list(set([i[2].capitalize() for i in self.indicators_list])))  # capitalize is called so that 'hazard' and 'Hazard' are considere the same


    def get_list_of_indicators_in_category(self,
                                           category):
        """Returns a list of indicators for a given category"""

        if category.capitalize() in self.get_list_of_categories():
            return [i for i in self.indicators_list if i[2].capitalize() == category.capitalize()]

        else:
            return None


    def get_dict_of_indicators_per_category(self):
        """Returns a dict grouping the indicators per category"""

        cats_dict = {}
        categories = self.get_list_of_categories()

        for category in categories:
            cats_dict[category] = self.get_list_of_indicators_in_category(category)

        return cats_dict


    def get_dict_of_indicator_names_per_category(self):
        """Returns a dict grouping the indicator names per category"""

        names_dict = {}
        categories = self.get_list_of_categories()

        for category in categories:
            names_dict[category] = [i[1] for i in self.get_list_of_indicators_in_category(category)]

        return names_dict


    def get_dict_of_indicator_codes_per_category(self):
        """Returns a dict grouping the indicator names per category"""

        codes_dict = {}
        categories = self.get_list_of_categories()

        for category in categories:
            codes_dict[category] = [i[0] for i in self.get_list_of_indicators_in_category(category)]

        return codes_dict




def copy_vector_layer(layer,
                      outputname,
                      vectortype):
    """Copies a vector layer"""

    features = [f for f in layer.getFeatures()]

    copylayer = QgsVectorLayer("{}?crs={}".format(vectortype, layer.crs().authid().lower()), outputname, "memory")

    data = copylayer.dataProvider()
    attr = layer.dataProvider().fields().toList()
    data.addAttributes(attr)
    copylayer.updateFields()
    data.addFeatures(features)

    QgsProject.instance().addMapLayer(copylayer)


def delete_fields(layer,
                  fields):
    """Deletes the fields of a vector layer"""

    to_delete = fields

    res = layer.dataProvider().deleteAttributes(to_delete)
    layer.updateFields()


def retain_fields(layer,
                  fields):
    """Retains the fields of a vector layer"""

    fields_ind = range(len(layer.fields().toList()))  # get indices of all fields (= list of number of fields)
    to_delete = [f for f in fields_ind if f not in fields]

    res = layer.dataProvider().deleteAttributes(to_delete)
    layer.updateFields()


def add_graduated_symbology(layer,
                            fieldName):
    """Add graduated symbology to layer"""

    sym = QgsSymbol.defaultSymbol(layer.geometryType())
    color_ramp = QgsGradientColorRamp(QColor("yellow"), QColor("red"))
    mode = QgsGraduatedSymbolRenderer.Pretty
    renderer = QgsGraduatedSymbolRenderer.createRenderer(layer, fieldName, 3, mode, sym, color_ramp)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def add_categorized_symbology(layer,
                              field,
                              colors):
    '''Add categorized symbology'''

    categories = []
    # svg = 'img/svg/accomodation-house.svg'
    # svg_sym = QgsSvgMarkerSymbolLayer(svg, 8)

    for level, color, label in colors:
        sym = QgsSymbol.defaultSymbol(layer.geometryType())
        sym.setColor(QColor(color))
        category = QgsRendererCategory(level, sym, label)
        categories.append(category)

    renderer = QgsCategorizedSymbolRenderer(field, categories)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def add_ranged_symbology(layer,
                         field,
                         colors):
    '''Add categorized symbology'''

    ranges = []
    # svg = 'img/svg/accomodation-house.svg'
    # svg_sym = QgsSvgMarkerSymbolLayer(svg, 8)

    for lower, upper, color, label in colors:
        sym = QgsSymbol.defaultSymbol(layer.geometryType())
        sym.setColor(QColor(color))
        rng = QgsRendererRange(lower, upper, sym, label)
        ranges.append(rng)

    renderer = QgsGraduatedSymbolRenderer(field, ranges)
    layer.setRenderer(renderer)
    layer.triggerRepaint()


def add_labels(layer,
               fieldName):
    """Add label to layer"""

    text = QgsTextFormat()
    text.setColor(QColor("black"))
    text.setSize(12)
    palayer = QgsPalLayerSettings()
    palayer.fieldName = fieldName
    palayer.placement = QgsPalLayerSettings.OverPoint
    palayer.drawLabels = True
    palayer.isExpression = True
    palayer.setFormat(text)

    layer.setLabelsEnabled(True)
    layer.setLabeling(QgsVectorLayerSimpleLabeling(palayer))
    layer.triggerRepaint()


def refactor_fields(layer,
                    names):
    """Rename field"""

    fields = [{'name': f.name(), 'type': f.type(), 'length': f.length(), 'precision': f.precision(), 'expression': '"{}"'.format(f.name())} for f in layer.fields()]
    oldnames = [n[0] for n in names]
    newnames = [n[1] for n in names]
    for f in fields:
        if f['name'] in oldnames:
            i = oldnames.index(f['name'])
            f['name'] = newnames[i]

    parameters = {'INPUT': layer,
                  'FIELDS_MAPPING': fields,
                  'OUTPUT': 'memory:'}

    processing.runAndLoadResults("qgis:refactorfields", parameters)


def set_null_to_zero(layer,
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
