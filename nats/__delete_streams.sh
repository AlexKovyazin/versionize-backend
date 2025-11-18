#!/bin/bash
set -euo pipefail

NATS_URL="nats://nats:4222"

echo "Check connection with Nats"
status=$(nats -s $NATS_URL account report connections)
if ! nats -s $NATS_URL account report connections > /dev/null 2>&1; then
  echo "No servers available for connection"
  exit 1
fi
echo "Connection exists"

echo "Deleting stream events"
if nats -s $NATS_URL stream rm events -f; then
  echo "Stream events is deleted"
else
  echo "Failed to delete stream events"
  exit 1
fi

echo "Deleting stream cmd"
if nats -s $NATS_URL stream rm cmd -f; then
  echo "Stream cmd is deleted"
else
  echo "Failed to delete stream cmd"
  exit 1
fi

echo "Done!"
