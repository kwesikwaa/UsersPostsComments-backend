from urllib import response
from httpx import URL
import typer
from enum import Enum
import requests


app = typer.Typer()

pressure_app = typer.Typer()
temperature_app = typer.Typer()

app.add_typer(pressure_app, name="pressure")
app.add_typer(temperature_app, name="temperature")


URL = "s"
response = requests.get(URL).json() 
sols = list(filter(lambda x: x.isnumeric(), response.keys()))
current_sol_data = response[sols[-1]]


class Hemisphere(Enum):
    north = "north"
    south = "south"

@app.command()
def season(hemisphere: Hemisphere):
    if hemisphere.value == "north":
        typer.echo(current_sol_data["Northern_season"])
    else:
        typer.echo(current_sol_data["Southern_season"])

if __name__=="__main__":
    app()