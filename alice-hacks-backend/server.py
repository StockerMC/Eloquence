from dataclasses import dataclass
from uuid import UUID
import main
from blacksheep import Application, json

app = Application()
get = app.router.get


# TODO: Create JSON structure


@get("/api")
def home(audio):
    #decrypt audio from base 64
    print(audio)

    return "test"
