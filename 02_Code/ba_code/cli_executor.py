import typer
from ba_code.web_scraping.tripadvisor_review import extractor

app = typer.Typer()


@app.command()
def extract_reviews():
    """
            \tThis command extracts online reviews from Tripadvisor
    """
    extractor.main()


@app.command()
def say_hello(name: str, iq: int, display_iq: bool = True):
    """
        Say hi to NAME, optionally with a --lastname.

        If --formal is used, say hi very formally.
    """
    typer.echo(f"Hello {name}")
    if display_iq:
        typer.echo(f"Your iq is {iq}")


if __name__ == "__main__":
    app()
