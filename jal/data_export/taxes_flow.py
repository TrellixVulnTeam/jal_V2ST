from datetime import datetime, timezone
from decimal import Decimal

from jal.db.account import JalAccount
from jal.db.asset import JalAsset
from jal.data_export.dlsg import DLSG


COUNTRY_NA_ID = 0
COUNTRY_RUSSIA_ID = 1


class TaxesFlowRus:
    def __init__(self):
        self.year_begin = 0
        self.year_end = 0
        self.flows = {}

    def prepare_flow_report(self, year):
        self.flows = {}
        self.year_begin = int(datetime.strptime(f"{year}", "%Y").replace(tzinfo=timezone.utc).timestamp())
        self.year_end = int(datetime.strptime(f"{year + 1}", "%Y").replace(tzinfo=timezone.utc).timestamp())

        # collect data for period start
        accounts = JalAccount.get_all_accounts(active_only=False)
        values = []
        for account in accounts:
            if account.country() == COUNTRY_NA_ID or account.country() == COUNTRY_RUSSIA_ID:
                continue
            assets = account.assets_list(self.year_begin)
            assets_value = Decimal('0')
            for asset_data in assets:
                assets_value += asset_data['amount'] * asset_data['asset'].quote(self.year_begin, account.currency())[1]
            if assets_value != Decimal('0'):
                values.append({
                    'account': account.number(),
                    'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': False,
                    'value': assets_value
                })
            money = account.get_asset_amount(self.year_begin, account.currency())
            if money != Decimal('0'):
                values.append({
                    'account': account.number(),
                    'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': True,
                    'value': money
                })
        values = sorted(values, key=lambda x: (x['account'], x['is_currency'], x['currency']))
        for item in values:
            self.append_flow_values(item, "begin")

        # collect data for period end
        # TODO - Optimize and combine with data collection for period start as routine is actually the same
        values = []
        for account in accounts:
            if account.country() == COUNTRY_NA_ID or account.country() == COUNTRY_RUSSIA_ID:
                continue
            assets = account.assets_list(self.year_end)
            assets_value = Decimal('0')
            for asset_data in assets:
                assets_value += asset_data['amount'] * asset_data['asset'].quote(self.year_end, account.currency())[1]
            if assets_value != Decimal('0'):
                values.append({
                    'account': account.number(),
                    'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': False,
                    'value': assets_value
                })
            money = account.get_asset_amount(self.year_end, account.currency())
            if money != Decimal('0'):
                values.append({
                    'account': account.number(),
                    'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': True,
                    'value': money
                })
        values = sorted(values, key=lambda x: (x['account'], x['is_currency'], x['currency']))
        for item in values:
            self.append_flow_values(item, "end")

        # collect money and assets ins/outs
        # FIXME - repetition of similar code and similar method calls - to be optimized
        for account in accounts:
            if account.country() == COUNTRY_NA_ID or account.country() == COUNTRY_RUSSIA_ID:
                continue
            money_in = account.money_flow_in(self.year_begin, self.year_end)
            if money_in != Decimal('0'):
                self.append_flow_values({
                    'account': account.number(), 'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': True, 'value': money_in
                }, "in")
            money_out = account.money_flow_out(self.year_begin, self.year_end)
            if money_out != Decimal('0'):
                self.append_flow_values({
                    'account': account.number(), 'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': True, 'value': money_out
                }, "out")
            assets_in = account.assets_flow_in(self.year_begin, self.year_end)
            if assets_in != Decimal('0'):
                self.append_flow_values({
                    'account': account.number(), 'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': False, 'value': assets_in
                }, "in")
            assets_out = account.assets_flow_out(self.year_begin, self.year_end)
            if assets_out != Decimal('0'):
                self.append_flow_values({
                    'account': account.number(), 'currency': JalAsset(account.currency()).symbol(),
                    'is_currency': False, 'value': assets_out
                }, "out")

        report = []
        for account in self.flows:
            for currency in self.flows[account]:
                record = self.flows[account][currency]
                row = {'report_template': "account_lines",
                       'account': account,
                       'currency': f"{currency} ({record['code']})",
                       'money': "Денежные средства",
                       'assets': "Финансовые активы"}
                for dtype in ['money', 'assets']:
                    for key in ['begin', 'in', 'out', 'end']:
                        param = f"{dtype}_{key}"
                        try:
                            row[param] = record[dtype][key] / Decimal('1000')
                        except KeyError:
                            row[param] = Decimal('0')
                report.append(row)
        return report

    # values are dictionary with keys {'account', 'currency', 'is_currency', 'value'}
    # this method puts it into self.flows array that has another structure:
    # { account: {currency: {0: {'value+suffix': X.XX}}, 1: {'value+suffix': SUM(X.XX)} } } }
    def append_flow_values(self, values, name):
        account = values['account']
        try:
            f_account = self.flows[account]
        except KeyError:
            f_account = self.flows[account] = {}
        currency = values['currency']
        try:
            f_currency = f_account[currency]
        except KeyError:
            try:
                currency_code = DLSG.currencies[currency]['code']
            except KeyError:
                currency_code = 'XXX'  # currency code isn't known
            f_currency = f_account[currency] = {'money': {}, 'assets': {}, 'code': currency_code}
        if values['is_currency'] == 0:
            try:
                f_currency['assets'][name] += values['value']
            except KeyError:
                f_currency['assets'][name] = values['value']
        else:                 # addition isn't required below as there should be only one value for money
            f_currency['money'][name] = values['value']
