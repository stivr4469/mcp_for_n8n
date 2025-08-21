from typer.testing import CliRunner
from cli.main import app

runner = CliRunner()

def test_parse_command():
    result = runner.invoke(app, ["parse", "run", "тест"])
    assert result.exit_code == 0
    assert "Парсим описание" in result.stdout