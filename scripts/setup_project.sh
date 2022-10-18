#!/bin/sh
set -ex
poetry install
pre-commit install --install-hooks
