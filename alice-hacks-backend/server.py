from dataclasses import dataclass
from uuid import UUID

from blacksheep import Application, json

app = Application()
get = app.router.get


# TODO: Create JSON structure
@dataclass
class Audio:
    id: UUID


@get("/api")
def home(request):
    return "GET Example"
