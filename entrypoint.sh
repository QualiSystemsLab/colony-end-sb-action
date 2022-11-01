#!/bin/sh -l

SANDBOX_ID=$1

echo "Running torque end sandbox command..."
torque --disable-version-check sb end ${SANDBOX_ID}
