"""Test peppier utilities."""

from pathlib import Path

from pytest import mark

from peppier import compact, identity, undent


@mark.parametrize(
    ('items', 'expected'),
    (
        ({}, {}),
        ({'a': None, 'b': 0, 'c': '', 'd': False, 'e': []}, {'b': 0, 'c': '', 'd': False, 'e': []}),
        ([('a', 1), ('b', None)], {'a': 1}),
    ),
    ids=('empty', 'falsy', 'pairs'),
)
def test_compact(items: dict | list, expected: dict) -> None:
    assert compact(items) == expected


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
