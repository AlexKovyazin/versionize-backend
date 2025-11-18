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

echo "Nats JetStream events stream creating"
if nats -s $NATS_URL stream add events --subjects "events.>" --ack --max-msgs=-1 --max-bytes=-1 --max-age=300s \
  --storage file --retention limits --max-msg-size=-1 --discard=old --replicas=1 \
  --max-msgs-per-subject=-1 --dupe-window=5m0s --no-allow-rollup --deny-delete --deny-purge; then
  echo "Stream events is successfully created"
else
  echo "Failed to create stream events"
  exit 1
fi
sleep 1s

echo "Nats JetStream cmd stream creating"
if nats -s $NATS_URL stream add cmd --subjects "cmd.>" --ack --max-msgs=-1 --max-bytes=-1 --max-age=300s \
  --storage file --retention limits --max-msg-size=-1 --discard=old --replicas=1 \
  --max-msgs-per-subject=-1 --dupe-window=5m0s --no-allow-rollup --deny-delete --deny-purge; then
  echo "Stream cmd is successfully created"
else
  echo "Failed to create stream cmd"
  exit 1
fi
sleep 1s

echo "Done!"
