import typer
from cli.commands import parse, generate, validate, deploy

app = typer.Typer(help="MSP CLI для управления workflow в N8N")

app.add_typer(parse.app, name="parse")
app.add_typer(generate.app, name="generate")
app.add_typer(validate.app, name="validate")
app.add_typer(deploy.app, name="deploy")

if __name__ == "__main__":
    app()