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
import os
import csv
import re


class Indicators():
    """Class for the PDRA Indicators.

    Format of Household PDRA Indicators CSV is:
    index   value
    0       INDICATOR_CODE
    1       INDICATOR_NAME
    2       CATEGORY
    3       RISK_VALUE
    """

    def __init__(self, indicators_path):
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


    def get_indicator_codes_from_indicators_list(self, indicators_list):

        return [i[0] for i in indicators_list]


    def get_indicator_names(self):

        return [i[1] for i in self.indicators_list]


    def get_indicator_names_from_indicators_list(self, indicators_list):

        return [i[1] for i in indicators_list]


    def get_indicator_name_from_code(self, indicator_code):
        """Returns the INDICATOR_NAME of the given INDICATOR_CODE"""

        if indicator_code in self.get_indicator_codes():  # if indicator_code exists, return the indicator_name
            return [i[1] for i in self.indicators_list if i[0] == indicator_code][0]
        else:
            return None


    def get_indicator_code_from_name(self, indicator_name):
        """Returns the INDICATOR_CODE of the given INDICATOR_NAME"""

        if indicator_name in self.get_indicator_names():  # if indicator_name exists, return the indicator_code
            return [i[0] for i in self.indicators_list if i[1] == indicator_name][0]
        else:
            return None


    def get_list_of_categories(self):
        """Returns the list of categories"""

        return sorted(list(set([i[2].capitalize() for i in self.indicators_list])))  # capitalize is called so that 'hazard' and 'Hazard' are considere the same


    def get_list_of_indicators_in_category(self, category):
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
