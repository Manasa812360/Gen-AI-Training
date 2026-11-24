#!/usr/bin/env bash
# SPECIFICATION (Lab 3.1) - let Copilot implement this below.
# health_check.sh: read-only health check for this Linux VM.
# - CPU: 1-minute load average vs number of cores (WARN > 1x cores, CRIT > 2x cores)
# - Memory: % used from /proc/meminfo (WARN > 80, CRIT > 90)
# - Disk: % used per mounted filesystem from df -P, excluding tmpfs/overlay (WARN > 80, CRIT > 90)
# - Services: nginx, docker, cron via systemctl is-active (CRIT if inactive)
# Output: aligned table CHECK | VALUE | STATUS, then "OVERALL: OK|WARN|CRIT"
# Exit codes: 0 OK, 1 WARN, 2 CRIT. Must not change anything on the system.
