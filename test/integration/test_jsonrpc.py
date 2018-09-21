import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from historiad import HistoriaDaemon
from historia_config import HistoriaConfig


def test_historiad():
    config_text = HistoriaConfig.slurp_config_file(config.historia_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000ffd590b1485b3caadc19b22e6379c733355108f107a430458cdf3407ab6'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'000008e378fa90a876bab78a957de006047db2725baf9ecdc96621cf6508ab7c'

    creds = HistoriaConfig.get_rpc_creds(config_text, network)
    historiad = HistoriaDaemon(**creds)
    assert historiad.rpc_command is not None

    assert hasattr(historiad, 'rpc_connection')

    # Historia testnet block 0 hash == 000008e378fa90a876bab78a957de006047db2725baf9ecdc96621cf6508ab7c
    # test commands without arguments
    info = historiad.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert historiad.rpc_command('getblockhash', 0) == genesis_hash
