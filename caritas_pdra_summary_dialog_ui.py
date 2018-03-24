# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'caritas_pdra_summary_dialog_ui.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from qgis import gui, core
from .resources_rc import *


class Ui_CaritasPDRASummaryDialog(object):
    def setupUi(self, CaritasPDRASummaryDialog):
        CaritasPDRASummaryDialog.setObjectName("CaritasPDRASummaryDialog")
        CaritasPDRASummaryDialog.resize(720, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CaritasPDRASummaryDialog.sizePolicy().hasHeightForWidth())
        CaritasPDRASummaryDialog.setSizePolicy(sizePolicy)
        CaritasPDRASummaryDialog.setMinimumSize(QtCore.QSize(720, 600))
        CaritasPDRASummaryDialog.setMaximumSize(QtCore.QSize(720, 600))
        font = QtGui.QFont()
        font.setPointSize(10)
        CaritasPDRASummaryDialog.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/plugins/caritas_pdra/img/icons/icon-summary.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        CaritasPDRASummaryDialog.setWindowIcon(icon)
        CaritasPDRASummaryDialog.setModal(False)
        self.label = QtWidgets.QLabel(CaritasPDRASummaryDialog)
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
        self.caritasLogo = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.caritasLogo.setGeometry(QtCore.QRect(640, 530, 71, 51))
        self.caritasLogo.setText("")
        self.caritasLogo.setPixmap(QtGui.QPixmap(":/plugins/caritas_pdra/img/logos/logo-nassa-caritas.png"))
        self.caritasLogo.setObjectName("caritasLogo")
        self.buttonBox = QtWidgets.QDialogButtonBox(CaritasPDRASummaryDialog)
        self.buttonBox.setGeometry(QtCore.QRect(540, 490, 171, 31))
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.selectHHLabel = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.selectHHLabel.setGeometry(QtCore.QRect(10, 10, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectHHLabel.setFont(font)
        self.selectHHLabel.setWordWrap(True)
        self.selectHHLabel.setObjectName("selectHHLabel")
        self.selectHHComboBox = gui.QgsMapLayerComboBox(CaritasPDRASummaryDialog)
        self.selectHHComboBox.setGeometry(QtCore.QRect(210, 10, 501, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectHHComboBox.setFont(font)
        self.selectHHComboBox.setStatusTip("")
        self.selectHHComboBox.setShowCrs(True)
        self.selectHHComboBox.setObjectName("selectHHComboBox")
        self.selectHHComboBox.setFilters(core.QgsMapLayerProxyModel.PointLayer)
        self.selectBoundaryLabel = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.selectBoundaryLabel.setGeometry(QtCore.QRect(10, 50, 191, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBoundaryLabel.setFont(font)
        self.selectBoundaryLabel.setWordWrap(True)
        self.selectBoundaryLabel.setObjectName("selectBoundaryLabel")
        self.selectBoundaryComboBox = gui.QgsMapLayerComboBox(CaritasPDRASummaryDialog)
        self.selectBoundaryComboBox.setGeometry(QtCore.QRect(210, 60, 501, 27))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBoundaryComboBox.setFont(font)
        self.selectBoundaryComboBox.setStatusTip("")
        self.selectBoundaryComboBox.setShowCrs(True)
        self.selectBoundaryComboBox.setObjectName("selectBoundaryComboBox")
        self.selectBoundaryComboBox.setFilters(core.QgsMapLayerProxyModel.PolygonLayer)
        self.filterByCategoryLabel = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.filterByCategoryLabel.setGeometry(QtCore.QRect(10, 160, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filterByCategoryLabel.setFont(font)
        self.filterByCategoryLabel.setWordWrap(True)
        self.filterByCategoryLabel.setObjectName("filterByCategoryLabel")
        self.filterByCategoryComboBox = QtWidgets.QComboBox(CaritasPDRASummaryDialog)
        self.filterByCategoryComboBox.setGeometry(QtCore.QRect(210, 160, 501, 31))
        self.filterByCategoryComboBox.setObjectName("filterByCategoryComboBox")
        self.summariesList = QtWidgets.QListWidget(CaritasPDRASummaryDialog)
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
        item = QtWidgets.QListWidgetItem()
        self.summariesList.addItem(item)
        self.summariesToCalculateLabel = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.summariesToCalculateLabel.setGeometry(QtCore.QRect(370, 220, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.summariesToCalculateLabel.setFont(font)
        self.summariesToCalculateLabel.setWordWrap(True)
        self.summariesToCalculateLabel.setObjectName("summariesToCalculateLabel")
        self.fieldsToSummarizeLabel = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.fieldsToSummarizeLabel.setGeometry(QtCore.QRect(10, 220, 351, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.fieldsToSummarizeLabel.setFont(font)
        self.fieldsToSummarizeLabel.setWordWrap(True)
        self.fieldsToSummarizeLabel.setObjectName("fieldsToSummarizeLabel")
        self.fieldsList = QtWidgets.QListWidget(CaritasPDRASummaryDialog)
        self.fieldsList.setGeometry(QtCore.QRect(10, 250, 341, 271))
        self.fieldsList.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.fieldsList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.fieldsList.setObjectName("fieldsList")
        self.note = QtWidgets.QLabel(CaritasPDRASummaryDialog)
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
        self.selectAllSummariesBtn = QtWidgets.QPushButton(CaritasPDRASummaryDialog)
        self.selectAllSummariesBtn.setGeometry(QtCore.QRect(510, 440, 91, 25))
        self.selectAllSummariesBtn.setObjectName("selectAllSummariesBtn")
        self.unselectAllSummariesBtn = QtWidgets.QPushButton(CaritasPDRASummaryDialog)
        self.unselectAllSummariesBtn.setGeometry(QtCore.QRect(620, 440, 91, 25))
        self.unselectAllSummariesBtn.setObjectName("unselectAllSummariesBtn")
        self.selectBoundaryIDFieldLabel = QtWidgets.QLabel(CaritasPDRASummaryDialog)
        self.selectBoundaryIDFieldLabel.setGeometry(QtCore.QRect(10, 100, 141, 51))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.selectBoundaryIDFieldLabel.setFont(font)
        self.selectBoundaryIDFieldLabel.setWordWrap(True)
        self.selectBoundaryIDFieldLabel.setObjectName("selectBoundaryIDFieldLabel")
        self.selectBoundaryIDFieldComboBox = gui.QgsFieldComboBox(CaritasPDRASummaryDialog)
        self.selectBoundaryIDFieldComboBox.setGeometry(QtCore.QRect(210, 110, 501, 27))
        self.selectBoundaryIDFieldComboBox.setObjectName("selectBoundaryIDFieldComboBox")
        self.note_2 = QtWidgets.QLabel(CaritasPDRASummaryDialog)
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

        self.retranslateUi(CaritasPDRASummaryDialog)
        QtCore.QMetaObject.connectSlotsByName(CaritasPDRASummaryDialog)

    def retranslateUi(self, CaritasPDRASummaryDialog):
        _translate = QtCore.QCoreApplication.translate
        CaritasPDRASummaryDialog.setWindowTitle(_translate("CaritasPDRASummaryDialog", "Summarize or Aggregate PDRA Data by Location (shp-vesion)"))
        self.label.setText(_translate("CaritasPDRASummaryDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">This plugin was made possible due to the efforts of NASSA/Caritas Philippines.</span></p></body></html>"))
        self.buttonBox.setToolTip(_translate("CaritasPDRASummaryDialog", "Perform Statistics Computation"))
        self.selectHHLabel.setToolTip(_translate("CaritasPDRASummaryDialog", "Siguraduhing ang coordinate reference system (hal. EPSG: 32651) ng household at admin layers ay pareho"))
        self.selectHHLabel.setText(_translate("CaritasPDRASummaryDialog", "Select Household Layer with PDRA Indicators"))
        self.selectHHComboBox.setToolTip(_translate("CaritasPDRASummaryDialog", "Piliin ang household layer na naglalaman ng mga PDRA indicators"))
        self.selectHHComboBox.setWhatsThis(_translate("CaritasPDRASummaryDialog", "Select the household point layer with PDRA indicators"))
        self.selectBoundaryLabel.setToolTip(_translate("CaritasPDRASummaryDialog", "Siguraduhing ang coordinate reference system (hal. EPSG: 32651) ng household at admin layers ay pareho"))
        self.selectBoundaryLabel.setText(_translate("CaritasPDRASummaryDialog", "Select the Boundary Layer for Grouping the Households"))
        self.selectBoundaryComboBox.setToolTip(_translate("CaritasPDRASummaryDialog", "Piliin ang layer na naglalaman ng administrative boundaries (hal. barangay, munisipalidad, lalawigan)"))
        self.selectBoundaryComboBox.setWhatsThis(_translate("CaritasPDRASummaryDialog", "Select the layer with the admin boundaries"))
        self.filterByCategoryLabel.setText(_translate("CaritasPDRASummaryDialog", "Filter Indicators by Category"))
        self.filterByCategoryComboBox.setToolTip(_translate("CaritasPDRASummaryDialog", "Pumili ng kategorya"))
        self.summariesList.setToolTip(_translate("CaritasPDRASummaryDialog", "Piliin ang mga istatistikang "))
        __sortingEnabled = self.summariesList.isSortingEnabled()
        self.summariesList.setSortingEnabled(False)
        item = self.summariesList.item(0)
        item.setText(_translate("CaritasPDRASummaryDialog", "Number of Households"))
        item.setToolTip(_translate("CaritasPDRASummaryDialog", "Bilang ng mga sambahayan"))
        item = self.summariesList.item(1)
        item.setText(_translate("CaritasPDRASummaryDialog", "Number of Households where Indicator is Present"))
        item.setToolTip(_translate("CaritasPDRASummaryDialog", "Bilang ng mga sambahayan na positibo sa napiling indicator"))
        item = self.summariesList.item(2)
        item.setText(_translate("CaritasPDRASummaryDialog", "Percentage of Households where Indicator is Present"))
        item.setToolTip(_translate("CaritasPDRASummaryDialog", "Porsyento ng mga sambahayan na positibo sa napiling indicator"))
        item = self.summariesList.item(3)
        item.setText(_translate("CaritasPDRASummaryDialog", "Number of Persons with Indicator Present"))
        item.setToolTip(_translate("CaritasPDRASummaryDialog", "Bilang ng mga tao na positibo sa napiling indicator"))
        self.summariesList.setSortingEnabled(__sortingEnabled)
        self.summariesToCalculateLabel.setText(_translate("CaritasPDRASummaryDialog", "Select Summaries to Compute"))
        self.fieldsToSummarizeLabel.setText(_translate("CaritasPDRASummaryDialog", "Select Indicator to Summarize"))
        self.fieldsList.setToolTip(_translate("CaritasPDRASummaryDialog", "Piliin ang mga indikador na gagamitin sa pagkwenta ng istatistika"))
        self.note.setText(_translate("CaritasPDRASummaryDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">* Make sure that the coordinate reference system (e.g. EPSG:32651) of the household and boundary layer are the same.</span></p></body></html>"))
        self.selectAllSummariesBtn.setText(_translate("CaritasPDRASummaryDialog", "Select All"))
        self.unselectAllSummariesBtn.setText(_translate("CaritasPDRASummaryDialog", "Unselect All"))
        self.selectBoundaryIDFieldLabel.setToolTip(_translate("CaritasPDRASummaryDialog", "Siguraduhing walang boundary o barangay na pareho ang pangalan"))
        self.selectBoundaryIDFieldLabel.setText(_translate("CaritasPDRASummaryDialog", "Unique Boundary ID (e.g. Barangay ID)"))
        self.selectBoundaryIDFieldComboBox.setToolTip(_translate("CaritasPDRASummaryDialog", "Pillin ang field kung saan nakalagay ang unique na ID ng boundary (e.g. BarangayID, MuniCityID)"))
        self.note_2.setText(_translate("CaritasPDRASummaryDialog", "<html><head/><body><p><span style=\" font-size:6pt;\">* Make sure that the boundary identification is unique for each feature in the layer</span></p></body></html>"))
