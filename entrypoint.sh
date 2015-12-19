#!/bin/bash
set -e

python wechat_treasure_ring/manage.py collectstatic --noinput

exec "$@"
