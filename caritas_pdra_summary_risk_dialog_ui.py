# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caritas_pdra_summary_risk_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qgis import gui, core
from .resources_rc import *


class Ui_CaritasPDRASummaryRiskDialog(object):
    def setupUi(self, CaritasPDRASummaryRiskDialog):
        CaritasPDRASummaryRiskDialog.setObjectName("CaritasPDRASummaryRiskDialog")
        CaritasPDRASummaryRiskDialog.resize(720, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CaritasPDRASummaryRiskDialog.sizePolicy().hasHeightForWidth())
        CaritasPDRASummaryRiskDialog.setSizePolicy(sizePolicy)
        CaritasPDRASummaryRiskDialog.setMinimumSize(QtCore.QSize(720, 600))
        CaritasPDRASummaryRiskDialog.setMaximumSize(QtCore.QSize(720, 600))
        font = QtGui.QFont()
        font.setPointSize(10)
        CaritasPDRASummaryRiskDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/caritas_pdra/img/icons/icon-summary-risk.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CaritasPDRASummaryRiskDialog.setWindowIcon(icon)
        CaritasPDRASummaryRiskDialog.setModal(False)
        self.label = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.label.setGeometry(QtCore.QRect(10, 530, 321, 51))
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(False)
        self.label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.caritasLogo = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.caritasLogo.setGeometry(QtCore.QRect(640, 530, 71, 51))
        self.caritasLogo.setText("")
        self.caritasLogo.setPixmap(QtGui.QPixmap(":/plugins/caritas_pdra/img/logos/logo-nassa-caritas.png"))
        self.caritasLogo.setObjectName("caritasLogo")
        self.buttonBox = QtWidgets.QDialogButtonBox(CaritasPDRASummaryRiskDialog)
        self.buttonBox.setGeometry(QtCore.QRect(540, 490, 171, 31))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.selectHHLabel = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.selectHHLabel.setGeometry(QtCore.QRect(10, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectHHLabel.setFont(font)
        self.selectHHLabel.setWordWrap(True)
        self.selectHHLabel.setObjectName("selectHHLabel")
        self.selectHHComboBox = gui.QgsMapLayerComboBox(CaritasPDRASummaryRiskDialog)
        self.selectHHComboBox.setGeometry(QtCore.QRect(210, 10, 501, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectHHComboBox.setFont(font)
        self.selectHHComboBox.setStatusTip("")
        self.selectHHComboBox.setShowCrs(True)
        self.selectHHComboBox.setObjectName("selectHHComboBox")
        self.selectHHComboBox.setFilters(core.QgsMapLayerProxyModel.PointLayer)
        self.selectBoundaryLabel = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.selectBoundaryLabel.setGeometry(QtCore.QRect(10, 50, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBoundaryLabel.setFont(font)
        self.selectBoundaryLabel.setWordWrap(True)
        self.selectBoundaryLabel.setObjectName("selectBoundaryLabel")
        self.selectBoundaryComboBox = gui.QgsMapLayerComboBox(CaritasPDRASummaryRiskDialog)
        self.selectBoundaryComboBox.setGeometry(QtCore.QRect(210, 60, 501, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBoundaryComboBox.setFont(font)
        self.selectBoundaryComboBox.setStatusTip("")
        self.selectBoundaryComboBox.setShowCrs(True)
        self.selectBoundaryComboBox.setObjectName("selectBoundaryComboBox")
        self.selectBoundaryComboBox.setFilters(core.QgsMapLayerProxyModel.PolygonLayer)
        self.filterByCategoryLabel = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.filterByCategoryLabel.setGeometry(QtCore.QRect(10, 160, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filterByCategoryLabel.setFont(font)
        self.filterByCategoryLabel.setWordWrap(True)
        self.filterByCategoryLabel.setObjectName("filterByCategoryLabel")
        self.filterByCategoryComboBox = QtWidgets.QComboBox(CaritasPDRASummaryRiskDialog)
        self.filterByCategoryComboBox.setGeometry(QtCore.QRect(210, 160, 501, 31))
        self.filterByCategoryComboBox.setObjectName("filterByCategoryComboBox")
        self.filterByCategoryComboBox.addItem("")
        self.filterByCategoryComboBox.addItem("")
        self.filterByCategoryComboBox.addItem("")
        self.summariesList = QtWidgets.QListWidget(CaritasPDRASummaryRiskDialog)
        self.summariesList.setGeometry(QtCore.QRect(370, 250, 341, 181))
        self.summariesList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.summariesList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.summariesList.setObjectName("summariesList")
        item = QtWidgets.QListWidgetItem()
        self.summariesList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.summariesList.addItem(item)
        item = QtWidgets.QListWidgetItem()
        self.summariesList.addItem(item)
        self.summariesToCalculateLabel = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.summariesToCalculateLabel.setGeometry(QtCore.QRect(370, 220, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.summariesToCalculateLabel.setFont(font)
        self.summariesToCalculateLabel.setWordWrap(True)
        self.summariesToCalculateLabel.setObjectName("summariesToCalculateLabel")
        self.fieldsToSummarizeLabel = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.fieldsToSummarizeLabel.setGeometry(QtCore.QRect(10, 220, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fieldsToSummarizeLabel.setFont(font)
        self.fieldsToSummarizeLabel.setWordWrap(True)
        self.fieldsToSummarizeLabel.setObjectName("fieldsToSummarizeLabel")
        self.fieldsList = QtWidgets.QListWidget(CaritasPDRASummaryRiskDialog)
        self.fieldsList.setGeometry(QtCore.QRect(10, 250, 341, 271))
        self.fieldsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fieldsList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.fieldsList.setObjectName("fieldsList")
        self.note = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.note.setGeometry(QtCore.QRect(210, 80, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.note.setFont(font)
        self.note.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.note.setScaledContents(False)
        self.note.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.note.setWordWrap(True)
        self.note.setObjectName("note")
        self.selectAllSummariesBtn = QtWidgets.QPushButton(CaritasPDRASummaryRiskDialog)
        self.selectAllSummariesBtn.setGeometry(QtCore.QRect(510, 440, 91, 25))
        self.selectAllSummariesBtn.setObjectName("selectAllSummariesBtn")
        self.unselectAllSummariesBtn = QtWidgets.QPushButton(CaritasPDRASummaryRiskDialog)
        self.unselectAllSummariesBtn.setGeometry(QtCore.QRect(620, 440, 91, 25))
        self.unselectAllSummariesBtn.setObjectName("unselectAllSummariesBtn")
        self.selectBoundaryIDFieldLabel = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.selectBoundaryIDFieldLabel.setGeometry(QtCore.QRect(10, 100, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBoundaryIDFieldLabel.setFont(font)
        self.selectBoundaryIDFieldLabel.setWordWrap(True)
        self.selectBoundaryIDFieldLabel.setObjectName("selectBoundaryIDFieldLabel")
        self.selectBoundaryIDFieldComboBox = gui.QgsFieldComboBox(CaritasPDRASummaryRiskDialog)
        self.selectBoundaryIDFieldComboBox.setGeometry(QtCore.QRect(210, 110, 501, 27))
        self.selectBoundaryIDFieldComboBox.setObjectName("selectBoundaryIDFieldComboBox")
        self.note_2 = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.note_2.setGeometry(QtCore.QRect(210, 130, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.note_2.setFont(font)
        self.note_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.note_2.setScaledContents(False)
        self.note_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.note_2.setWordWrap(True)
        self.note_2.setObjectName("note_2")
        self.note_3 = QtWidgets.QLabel(CaritasPDRASummaryRiskDialog)
        self.note_3.setGeometry(QtCore.QRect(210, 30, 501, 31))
        font = QtGui.QFont()
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.note_3.setFont(font)
        self.note_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.note_3.setScaledContents(False)
        self.note_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.note_3.setWordWrap(True)
        self.note_3.setObjectName("note_3")

        self.retranslateUi(CaritasPDRASummaryRiskDialog)
        QtCore.QMetaObject.connectSlotsByName(CaritasPDRASummaryRiskDialog)

    def retranslateUi(self, CaritasPDRASummaryRiskDialog):
        _translate = QtCore.QCoreApplication.translate
        CaritasPDRASummaryRiskDialog.setWindowTitle(_translate("CaritasPDRASummaryRiskDialog", "Statistics on Hazard, Vulnerability, Capacity, and Risk Computed from PDRA Data (shp-version)"))
        self.label.setText(_translate("CaritasPDRASummaryRiskDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">This plugin was made possible due to the efforts of NASSA/Caritas Philippines.</span></p></body></html>"))
        self.buttonBox.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Perform Statistics Computation"))
        self.selectHHLabel.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Siguraduhing ang coordinate reference system (hal. EPSG: 32651) ng household at admin layers ay pareho"))
        self.selectHHLabel.setText(_translate("CaritasPDRASummaryRiskDialog", "Select Household Layer with Risk Levels"))
        self.selectHHComboBox.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Piliin ang household layer na naglalaman ng mga Risk Levels (Ito ang mga resulta ng Caritas PDRA Risk Computation)"))
        self.selectHHComboBox.setWhatsThis(_translate("CaritasPDRASummaryRiskDialog", "Select the household point layer with PDRA indicators"))
        self.selectBoundaryLabel.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Siguraduhing ang coordinate reference system (hal. EPSG: 32651) ng household at admin layers ay pareho"))
        self.selectBoundaryLabel.setText(_translate("CaritasPDRASummaryRiskDialog", "Select the Boundary Layer for Grouping the Households"))
        self.selectBoundaryComboBox.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Piliin ang layer na naglalaman ng administrative boundaries (hal. barangay, munisipalidad, lalawigan)"))
        self.selectBoundaryComboBox.setWhatsThis(_translate("CaritasPDRASummaryRiskDialog", "Select the layer with the admin boundaries"))
        self.filterByCategoryLabel.setText(_translate("CaritasPDRASummaryRiskDialog", "Filter Level To Show"))
        self.filterByCategoryComboBox.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Pumili ng kategorya"))
        self.filterByCategoryComboBox.setItemText(0, _translate("CaritasPDRASummaryRiskDialog", "LOW"))
        self.filterByCategoryComboBox.setItemText(1, _translate("CaritasPDRASummaryRiskDialog", "MEDIUM"))
        self.filterByCategoryComboBox.setItemText(2, _translate("CaritasPDRASummaryRiskDialog", "HIGH"))
        self.summariesList.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Piliin ang mga istatistikang kukwentahin"))
        __sortingEnabled = self.summariesList.isSortingEnabled()
        self.summariesList.setSortingEnabled(False)
        item = self.summariesList.item(0)
        item.setText(_translate("CaritasPDRASummaryRiskDialog", "Number of Households"))
        item.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Bilang ng mga sambahayan"))
        item = self.summariesList.item(1)
        item.setText(_translate("CaritasPDRASummaryRiskDialog", "Number of Households at Risk"))
        item.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Bilang ng mga sambahayan na nasa ilalim ng napiling lebel ng Panganib (Risk Level)"))
        item = self.summariesList.item(2)
        item.setText(_translate("CaritasPDRASummaryRiskDialog", "Percentage of Households at Risk"))
        item.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Porsyento ng mga sambahayan na nasa ilalim ng napiling lebel ng Panganib (Risk Level)"))
        self.summariesList.setSortingEnabled(__sortingEnabled)
        self.summariesToCalculateLabel.setText(_translate("CaritasPDRASummaryRiskDialog", "Select Summaries to Compute"))
        self.fieldsToSummarizeLabel.setText(_translate("CaritasPDRASummaryRiskDialog", "Select Indicator to Summarize"))
        self.fieldsList.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Piliin ang mga indikador na gagamitin sa pagkwenta ng istatistika"))
        self.note.setText(_translate("CaritasPDRASummaryRiskDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">* Make sure that the coordinate reference system (e.g. EPSG:32651) of the risk level and boundary layer are the same.</span></p></body></html>"))
        self.selectAllSummariesBtn.setText(_translate("CaritasPDRASummaryRiskDialog", "Select All"))
        self.unselectAllSummariesBtn.setText(_translate("CaritasPDRASummaryRiskDialog", "Unselect All"))
        self.selectBoundaryIDFieldLabel.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Siguraduhing walang boundary o barangay na pareho ang pangalan"))
        self.selectBoundaryIDFieldLabel.setText(_translate("CaritasPDRASummaryRiskDialog", "Unique Boundary ID (e.g. Barangay ID)"))
        self.selectBoundaryIDFieldComboBox.setToolTip(_translate("CaritasPDRASummaryRiskDialog", "Pillin ang field kung saan nakalagay ang unique na ID ng boundary (e.g. BarangayID, MuniCityID)"))
        self.note_2.setText(_translate("CaritasPDRASummaryRiskDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">* Make sure that the boundary identification is unique for each feature in the layer</span></p></body></html>"))
        self.note_3.setText(_translate("CaritasPDRASummaryRiskDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">* Result of the Caritas PDRA Risk Computation Tool</span></p></body></html>"))
