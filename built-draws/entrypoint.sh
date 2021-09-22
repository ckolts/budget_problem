#!/bin/bash

set -euo pipefail

# wait for database to be ready
wait-for-it -t 30 built-mysql:3306

pipenv run flask run --no-debugger --reload --without-threads
