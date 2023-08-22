from config import Config

import pytest
import requests
import uuid


@pytest.fixture
def rid():
    return str(uuid.uuid4())


def test_rid_required():
    headers = {
        # no "X-Request-ID" header
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 400


def test_api_key_required(rid):
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        # Try to reach the Ramistat Core directly
        f"{Config.RamistatCore.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 401


def test_diagnostic_success(rid):
    # TODO regular syntax error somewhere here? 
    # Check diagnostics
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    location, _, ontarian_manifold, kpg = diagnostic.text.split()
    # Depending on where tests left off, The Rascal may in these locations
    assert location in ("Earth", "Ni'Var", "Betazed")
    # All relevant tests cool after
    assert int(ontarian_manifold) == 40000


def test_warp_and_cool_success(rid):
    # TODO can use warp fn for doc syntax lookup
    # location = req.get_media()["location"]
    # But then we can't test the 40000kpgs assumption

    # Send warp command
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/json",
        "Accept": "text/plain"
    }
    warp = requests.put(
        f"{Config.IsopalavialInterface.uri}/warp",
        headers=headers,
        json={"location": "Ni'Var"},
    )
    assert warp.status_code == 200
    assert warp.text == "Engage!"

    # Check diagnostics
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    location, _, ontarian_manifold, kpg = diagnostic.text.split()
    assert location == ("Ni'Var")
    assert int(ontarian_manifold) != 40000


    # Send cool command
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    cool = requests.put(
        f"{Config.IsopalavialInterface.uri}/cool",
        headers=headers,
    )
    assert cool.status_code == 200
    assert cool.text == "Cooled!"

    # Check diagnostics
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    location, _, ontarian_manifold, kpg = diagnostic.text.split()
    assert location == ("Ni'Var")
    assert int(ontarian_manifold) == 40000


def test_multiwarp_fail(rid):
    # Send warp command
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/json",
        "Accept": "text/plain"
    }
    warp = requests.put(
        f"{Config.IsopalavialInterface.uri}/warp",
        headers=headers,
        json={"location": "Ni'Var"},
    )
    assert warp.status_code == 200
    assert warp.text == "Engage!"

    # Check diagnostics
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    location, _, ontarian_manifold, kpg = diagnostic.text.split()
    assert location == ("Ni'Var")
    assert int(ontarian_manifold) != 40000

    # Send warp command without proper ontarian manifold value
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/json",
        "Accept": "text/plain"
    }
    warp = requests.put(
        f"{Config.IsopalavialInterface.uri}/warp",
        headers=headers,
        json={"location": "Betazed"},
    )
    assert warp.status_code == 500
    assert warp.text == ""

    # Check diagnostics - we have not moved
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    _location, _, _ontarian_manifold, kpg = diagnostic.text.split()
    assert location == _location
    assert ontarian_manifold == _ontarian_manifold

    # Send cool command to not interfere with other tests
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    cool = requests.put(
        f"{Config.IsopalavialInterface.uri}/cool",
        headers=headers,
    )
    assert cool.status_code == 200
    assert cool.text == "Cooled!"


def test_multi_warp_success(rid):
    # Send warp command
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/json",
        "Accept": "text/plain"
    }
    warp = requests.put(
        f"{Config.IsopalavialInterface.uri}/warp",
        headers=headers,
        json={"location": "Ni'Var"},
    )
    assert warp.status_code == 200
    assert warp.text == "Engage!"

    # Check diagnostics
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    location, _, ontarian_manifold, kpg = diagnostic.text.split()
    assert location == ("Ni'Var")
    assert int(ontarian_manifold) != 40000

    # Send cool command to ready another warp
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    cool = requests.put(
        f"{Config.IsopalavialInterface.uri}/cool",
        headers=headers,
    )
    assert cool.status_code == 200
    assert cool.text == "Cooled!"

    # Send warp command
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/json",
        "Accept": "text/plain"
    }
    warp = requests.put(
        f"{Config.IsopalavialInterface.uri}/warp",
        headers=headers,
        json={"location": "Betazed"},
    )
    assert warp.status_code == 200
    assert warp.text == "Engage!"

    # Check diagnostics - we have not moved
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    diagnostic = requests.get(
        f"{Config.IsopalavialInterface.uri}/diagnostic",
        headers=headers,
    )
    assert diagnostic.status_code == 200
    location, _, ontarian_manifold, kpg = diagnostic.text.split()
    assert location == ("Betazed")
    assert int(ontarian_manifold) != 40000

    # Send cool command to not interfere with other tests
    headers = {
        "X-Request-ID": rid,
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain"
    }
    cool = requests.put(
        f"{Config.IsopalavialInterface.uri}/cool",
        headers=headers,
    )
    assert cool.status_code == 200
    assert cool.text == "Cooled!"
