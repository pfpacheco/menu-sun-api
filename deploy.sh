#!/usr/bin/env bash
make deploy/tunnel TUNNEL_PORT=10000
make db/migrate DB_HOST=127.0.0.1 DB_PORT=10000 DB_NAME=${DB_NAME}
make deploy