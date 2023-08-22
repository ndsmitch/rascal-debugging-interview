

class IsopalavialInterface:
    scheme = "http"
    host = "localhost"
    port = 8000
    uri = f"{scheme}://{host}:{port}"


class FiromactalDrive:
    scheme = "http"
    host = "localhost"
    port = 8111
    uri = f"{scheme}://{host}:{port}"


class RamistatCore:
    scheme = "http"
    host = "localhost"
    port = 8222
    uri = f"{scheme}://{host}:{port}"


class OntarianManifold:
    path = "ontarian_manifold"


class Location:
    path = "location"


class Config:
    IsopalavialInterface = IsopalavialInterface()
    FiromactalDrive = FiromactalDrive()
    RamistatCore = RamistatCore()
    OntarianManifold = OntarianManifold()
    Location = Location()
