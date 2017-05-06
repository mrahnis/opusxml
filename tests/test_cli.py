from click.testing import CliRunner

import opusxml
from opusxml.cli.opusxml import cli

def test_opusxml():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
