import json

from tests.fixtures import project_root, data_path, prepare_db, prepare_db_ibkr, prepare_db_xls
from data_import.broker_statements.ibkr import StatementIBKR
from data_import.broker_statements.uralsib import StatementUKFU
from data_import.broker_statements.kit import StatementKIT
from data_import.broker_statements.psb import StatementPSB
from data_import.broker_statements.openbroker import StatementOpenBroker
from data_import.broker_statements.just2trade import StatementJ2T
from data_import.broker_statements.open_portfolio import StatementOpenPortfolio

from constants import PredefinedAsset
from tests.helpers import create_assets


# ----------------------------------------------------------------------------------------------------------------------
def test_statement_ibkr(tmp_path, project_root, data_path, prepare_db_ibkr):
    # Test big major things
    with open(data_path + 'ibkr.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)
    IBKR = StatementIBKR()
    IBKR.load(data_path + 'ibkr.xml')
    assert IBKR._data == statement

    # Test rights issue and vesting
    with open(data_path + 'ibkr_rights_vesting.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)
    IBKR = StatementIBKR()
    IBKR.load(data_path + 'ibkr_rights_vesting.xml')
    assert IBKR._data == statement


# ----------------------------------------------------------------------------------------------------------------------
def test_statement_uralsib(tmp_path, project_root, data_path, prepare_db_xls):
    with open(data_path + 'ukfu.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)

    UKFU = StatementUKFU()
    UKFU.load(data_path + 'ukfu.zip')
    assert UKFU._data == statement


# ----------------------------------------------------------------------------------------------------------------------
def test_statement_kit(tmp_path, project_root, data_path, prepare_db_xls):
    with open(data_path + 'kit.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)

    KIT = StatementKIT()
    KIT.load(data_path + 'kit.xlsx')
    assert KIT._data == statement


# ----------------------------------------------------------------------------------------------------------------------
def test_statement_psb(tmp_path, project_root, data_path, prepare_db_xls):
    with open(data_path + 'psb.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)

    PSB = StatementPSB()
    PSB.load(data_path + 'psb.xlsx')
    assert PSB._data == statement


# ----------------------------------------------------------------------------------------------------------------------
def test_statement_open(tmp_path, project_root, data_path, prepare_db_xls):
    with open(data_path + 'open.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)

    OpenBroker = StatementOpenBroker()
    OpenBroker.load(data_path + 'open.xml')
    assert OpenBroker._data == statement


# ----------------------------------------------------------------------------------------------------------------------
def test_statement_just2trade(tmp_path, project_root, data_path, prepare_db_xls):
    create_assets([(5, 'JNJ', 'JOHNSON & JOHNSON', 'US4781601046', 1, PredefinedAsset.Stock, 0)])

    with open(data_path + 'j2t.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)

    J2T = StatementJ2T()
    J2T.load(data_path + 'j2t.xlsx')
    assert J2T._data == statement

def test_statement_open_portfolio(tmp_path, project_root, data_path):
    with open(data_path + 'pof_converted.json', 'r', encoding='utf-8') as json_file:
        statement = json.load(json_file)

    OpenPortfolio = StatementOpenPortfolio()
    OpenPortfolio.load(data_path + 'pof.json')
    assert OpenPortfolio._data == statement
