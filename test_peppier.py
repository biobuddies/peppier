"""Test peppier utilities."""

from collections.abc import Callable
from os import getenv
from pathlib import Path

from numpy import array
from pandas import DataFrame
from pytest import MonkeyPatch, mark

from peppier import compact, identity, undent


@mark.parametrize(
    ('mapping', 'kwargs', 'expected'),
    (
        ({}, {}, {}),
        (
            {'a': None, 'b': 0, 'c': '', 'd': False, 'e': [], 'f': b'', 'g': ' '},
            {},
            {'b': 0, 'd': False, 'e': [], 'g': ' '},
        ),
        (None, {'a': None, 'b': 0}, {'b': 0}),
        ({1: 'one', 'a': 'a'}, {'a': None, 'b': 'b'}, {1: 'one', 'b': 'b'}),
    ),
    ids=('empty', 'mapping', 'keywords', 'keywords-override-mapping'),
)
def test_compact(mapping: dict | None, kwargs: dict, expected: dict) -> None:
    assert compact(mapping, **kwargs) == expected


@mark.parametrize('value', (array([1, 2]), DataFrame({'a': [1, 2]})), ids=('numpy', 'pandas'))
def test_compact_ambiguous(value: object) -> None:
    """Keep values whose truth value or == '' raises ValueError."""
    assert compact(value=value)['value'] is value


def test_compact_environment(monkeypatch: MonkeyPatch) -> None:
    """Forward only set variables, like measles test_integration.py downstream_environment()."""
    monkeypatch.delenv('GITHUB_TOKEN', raising=False)
    monkeypatch.setenv('SSL_CERT_FILE', '/etc/ssl/cert.pem')
    assert (
        compact({
            'GITHUB_TOKEN': getenv('GITHUB_TOKEN'),
            'HOME': '/home/user',
            'SSL_CERT_FILE': getenv('SSL_CERT_FILE'),
        })
        == compact(
            GITHUB_TOKEN=getenv('GITHUB_TOKEN'),
            HOME='/home/user',
            SSL_CERT_FILE=getenv('SSL_CERT_FILE'),
        )
        == {'HOME': '/home/user', 'SSL_CERT_FILE': '/etc/ssl/cert.pem'}
    )


@mark.parametrize('value', (None, 0, '', [], object()))
def test_identity(value: object) -> None:
    assert identity(value) is value


@mark.parametrize(
    ('transform', 'expected'),
    ((str.upper, ['B', 'A']), (identity, ['b', 'a'])),
    ids=('upper', 'identity'),
)
def test_identity_map(transform: Callable[[str], str], expected: list[str]) -> None:
    """Callers choosing a transform need not special-case leaving values alone."""
    assert list(map(transform, ['b', 'a'])) == expected


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
