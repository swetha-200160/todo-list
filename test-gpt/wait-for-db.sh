#!/usr/bin/env bash
set -e
host="$MYSQL_HOST"
until mysqladmin ping -h"$host" --silent; do
  echo "⏳ Waiting for MySQL at $host..."
  sleep 2
done
echo "✅ MySQL is up!"
exec "$@"
