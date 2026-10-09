"""Test peppier utilities."""

from os import getenv
from pathlib import Path

from pytest import MonkeyPatch, mark

from peppier import compact, identity, undent


@mark.parametrize(
    ('mapping', 'expected'),
    (
        ({}, {}),
        ({'a': None, 'b': 0, 'c': '', 'd': False, 'e': []}, {'b': 0, 'c': '', 'd': False, 'e': []}),
    ),
    ids=('empty', 'falsy'),
)
def test_compact(mapping: dict, expected: dict) -> None:
    assert compact(mapping) == expected


def test_compact_environment(monkeypatch: MonkeyPatch) -> None:
    """Forward only set variables, like measles test_integration.py downstream_environment()."""
    monkeypatch.delenv('GITHUB_TOKEN', raising=False)
    monkeypatch.setenv('NO_PROXY', '')
    monkeypatch.setenv('SSL_CERT_FILE', '/etc/ssl/cert.pem')
    assert compact({
        'GITHUB_TOKEN': getenv('GITHUB_TOKEN'),
        'HOME': '/home/user',
        **{name: getenv(name) for name in ('NO_PROXY', 'SSL_CERT_FILE')},
    }) == {'HOME': '/home/user', 'NO_PROXY': '', 'SSL_CERT_FILE': '/etc/ssl/cert.pem'}


@mark.parametrize('value', (None, 0, '', [], object()))
def test_identity(value: object) -> None:
    assert identity(value) is value


@mark.parametrize(
    ('string', 'path'),
    (
        (
            """
            terraform {
              required_providers {
                docker = {
                  source  = "kreuzwerker/docker"
                  version = "3.4.0"
                }
              }
            }

            provider "docker" {}

            resource "docker_image" "nginxImage" {
              name         = "nginx:latest"
              keep_locally = false
            }

            resource "docker_container" "nginxContainer" {
              name  = "tutorial"
              image = docker_image.nginxImage.name
              ports {
                internal = 80
                external = 8000
              }
            }
            """,
            'tests/docker.tf',
        ),
        (
            """
            <pre style="font-family: monospace; line-height: 1.275">
              E   A   D   G   B   e
              ✕           ◯       ◯
              ┌───┬───┬───┬───┬───┐
            1 │   │   │   │   ●   │
              ├───┼───┼───┼───┼───┤
            2 │   │   ●   │   │   │
              ├───┼───┼───┼───┼───┤
            3 │   ●   │   │   │   │
              ├───┼───┼───┼───┼───┤
            4 │   │   │   │   │   │
              └───┴───┴───┴───┴───┘
            </pre>
            """,
            'tests/fretboard.html',
        ),
    ),
    ids=('terraform', 'fretboard'),
)
def test_undent(string: str, path: str) -> None:
    assert undent(string) == Path(path).read_text()
