from functools import partial
from datetime import datetime
import logging

from PySide6.QtCore import Property, Slot
from PySide6.QtWidgets import QFileDialog
from jal.ui.ui_tax_export_widget import Ui_TaxWidget
from jal.widgets.mdi import MdiWidget
from jal.data_export.taxes import TaxesRus
from jal.data_export.xlsx import XLSX
from jal.data_export.dlsg import DLSG


class TaxWidget(MdiWidget, Ui_TaxWidget):
    def __init__(self, parent):
        MdiWidget.__init__(self)
        self.setupUi(self)

        self.XlsSelectBtn.pressed.connect(partial(self.OnFileBtn, 'XLS-OUT'))
        self.InitialSelectBtn.pressed.connect(partial(self.OnFileBtn, 'DLSG-IN'))
        self.OutputSelectBtn.pressed.connect(partial(self.OnFileBtn, 'DLSG-OUT'))
        self.SaveButton.pressed.connect(self.SaveReport)

        # center dialog with respect to parent window
        x = parent.x() + parent.width() / 2 - self.width() / 2
        y = parent.y() + parent.height() / 2 - self.height() / 2
        self.setGeometry(x, y, self.width(), self.height())

    @Slot()
    def OnFileBtn(self, type):
        selector = {
            'XLS-OUT': (self.tr("Save tax reports to:"), self.tr("Excel files (*.xlsx)"), '.xlsx', self.XlsFileName),
            'DLSG-IN': (self.tr("Get tax form template from:"), self.tr("Tax form 2020 (*.dc0)"),
                        '.dc0', self.DlsgInFileName),
            'DLSG-OUT': (self.tr("Save tax form to:"), self.tr("Tax form 2020 (*.dc0)"), '.dc0', self.DlsgOutFileName)
        }
        if type[-3:] == '-IN':
            filename = QFileDialog.getOpenFileName(self, selector[type][0], ".", selector[type][1])
        elif type[-4:] == '-OUT':
            filename = QFileDialog.getSaveFileName(self, selector[type][0], ".", selector[type][1])
        else:
            raise ValueError
        if filename[0]:
            if filename[1] == selector[type][1] and filename[0][-len(selector[type][2]):] != selector[type][2]:
                selector[type][3].setText(filename[0] + selector[type][2])
            else:
                selector[type][3].setText(filename[0])

    def getYear(self):
        return self.Year.value()

    def getXlsFilename(self):
        return self.XlsFileName.text()

    def getAccount(self):
        return self.AccountWidget.selected_id

    def getDlsgState(self):
        return self.DlsgGroup.isChecked()

    def getDslgInFilename(self):
        return self.DlsgInFileName.text()

    def getDslgOutFilename(self):
        return self.DlsgOutFileName.text()

    def getBrokerAsIncomeName(self):
        return self.IncomeSourceBroker.isChecked()

    def getDividendsOnly(self):
        return self.DividendsOnly.isChecked()

    def getNoSettlement(self):
        return self.NoSettlement.isChecked()

    year = Property(int, fget=getYear)
    xls_filename = Property(str, fget=getXlsFilename)
    account = Property(int, fget=getAccount)
    update_dlsg = Property(bool, fget=getDlsgState)
    dlsg_in_filename = Property(str, fget=getDslgInFilename)
    dlsg_out_filename = Property(str, fget=getDslgOutFilename)
    dlsg_broker_as_income = Property(bool, fget=getBrokerAsIncomeName)
    dlsg_dividends_only = Property(bool, fget=getDividendsOnly)
    no_settelement = Property(bool, fget=getNoSettlement)

    def SaveReport(self):
        taxes = TaxesRus()
        tax_report = taxes.prepare_tax_report(self.year, self.account)

        reports_xls = XLSX(self.xls_filename)
        templates = {
            "Дивиденды": "tax_rus_dividends.json",
            "Акции": "tax_rus_trades.json",
            "Облигации": "tax_rus_bonds.json",
            "ПФИ": "tax_rus_derivatives.json",
            "Корп.события": "tax_rus_corporate_actions.json",
            "Комиссии": "tax_rus_fees.json",
            "Проценты": "tax_rus_interests.json"
        }
        parameters = {
            "period": f"{datetime.utcfromtimestamp(taxes.year_begin).strftime('%d.%m.%Y')}"
                      f" - {datetime.utcfromtimestamp(taxes.year_end - 1).strftime('%d.%m.%Y')}",
            "account": f"{taxes.account_number} ({taxes.account_currency})",
            "currency": taxes.account_currency
        }
        for section in tax_report:
            if section not in templates:
                continue
            reports_xls.output_data(tax_report[section], templates[section], parameters)
        reports_xls.save()

        logging.info(self.tr("Tax report saved to file ") + f"'{self.xls_filename}'")

        if self.update_dlsg:
            tax_forms = DLSG(only_dividends=self.dlsg_dividends_only)
            try:
                tax_forms.read_file(self.dlsg_in_filename)
            except:
                logging.error(self.tr("Can't open tax form file ") + f"'{self.dlsg_in_filename}'")
                return
            tax_forms.update_taxes(tax_report)
            try:
                tax_forms.write_file(self.dlsg_out_filename)
            except:
                logging.error(self.tr("Can't write tax form into file ") + f"'{self.dlsg_out_filename}'")
