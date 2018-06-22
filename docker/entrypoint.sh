#!/bin/bash

set -e #  Exit immediately if a command exits with a non-zero status.
exec tail -f /etc/hosts
