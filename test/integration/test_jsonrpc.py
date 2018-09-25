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
    genesis_hash = u'00000eabb15c5ad6e93847c3913bc312c716e16e6c0158de004d53df1f58067f'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'0000001bb8252117d7b1bb13cc2e8abb766b0ac68cc855830f9d7fb6072d7b10'

    creds = HistoriaConfig.get_rpc_creds(config_text, network)
    historiad = HistoriaDaemon(**creds)
    assert historiad.rpc_command is not None

    assert hasattr(historiad, 'rpc_connection')

    # Historia testnet block 0 hash == 0000001bb8252117d7b1bb13cc2e8abb766b0ac68cc855830f9d7fb6072d7b10
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
