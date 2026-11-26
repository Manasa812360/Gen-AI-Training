#!/usr/bin/env bash
# SPECIFICATION (Lab 3.1) - let Copilot implement this below.
# health_check.sh: read-only health check for this Linux VM.
# - CPU: 1-minute load average vs number of cores (WARN > 1x cores, CRIT > 2x cores)
# - Memory: % used from /proc/meminfo (WARN > 80, CRIT > 90)
# - Disk: % used per mounted filesystem from df -P, excluding tmpfs/overlay (WARN > 80, CRIT > 90)
# - Services: nginx, docker, cron via systemctl is-active (CRIT if inactive)
# Output: aligned table CHECK | VALUE | STATUS, then "OVERALL: OK|WARN|CRIT"
# Exit codes: 0 OK, 1 WARN, 2 CRIT. Must not change anything on the system.

set -euo pipefail

export LC_ALL=C

overall=0
check_width=5
value_width=5
checks=()
values=()
statuses=()

record() {
    local check=$1
    local value=$2
    local status=$3
    local severity=0

    case "$status" in
        WARN) severity=1 ;;
        CRIT) severity=2 ;;
    esac

    checks+=("$check")
    values+=("$value")
    statuses+=("$status")
    ((${#check} > check_width)) && check_width=${#check}
    ((${#value} > value_width)) && value_width=${#value}
    if ((severity > overall)); then
        overall=$severity
    fi
}

status_for_percent() {
    local value=$1

    if awk -v value="$value" 'BEGIN { exit !(value > 90) }'; then
        printf 'CRIT'
    elif awk -v value="$value" 'BEGIN { exit !(value > 80) }'; then
        printf 'WARN'
    else
        printf 'OK'
    fi
}

# A normalized load of 1 means all available CPU cores are fully occupied.
if [[ -r /proc/loadavg ]] && cores=$(getconf _NPROCESSORS_ONLN 2>/dev/null); then
    cpu_load=$(awk 'NR == 1 { print $1 }' /proc/loadavg)
    if [[ $cpu_load =~ ^[0-9]+([.][0-9]+)?$ ]] &&
        [[ $cores =~ ^[1-9][0-9]*$ ]]; then
        load_per_core=$(awk -v cpu_load="$cpu_load" -v cores="$cores" \
            'BEGIN { printf "%.2f", cpu_load / cores }')
        if awk -v cpu_load="$cpu_load" -v cores="$cores" \
            'BEGIN { exit !(cpu_load > 2 * cores) }'; then
            cpu_status=CRIT
        elif awk -v cpu_load="$cpu_load" -v cores="$cores" \
            'BEGIN { exit !(cpu_load > cores) }'; then
            cpu_status=WARN
        else
            cpu_status=OK
        fi
        record "CPU load (1m / cores)" "$cpu_load / $cores ($load_per_core)" "$cpu_status"
    else
        record "CPU load (1m / cores)" "unavailable" "CRIT"
    fi
else
    record "CPU load (1m / cores)" "unavailable" "CRIT"
fi

if [[ -r /proc/meminfo ]]; then
    memory_used=$(awk '
        /^MemTotal:/ { total = $2 }
        /^MemAvailable:/ { available = $2 }
        END {
            if (total > 0 && available >= 0)
                printf "%.1f", 100 * (total - available) / total
            else
                exit 1
        }
    ' /proc/meminfo) || memory_used=

    if [[ $memory_used =~ ^[0-9]+([.][0-9]+)?$ ]]; then
        record "Memory used" "${memory_used}%" "$(status_for_percent "$memory_used")"
    else
        record "Memory used" "unavailable" "CRIT"
    fi
else
    record "Memory used" "unavailable" "CRIT"
fi

if disk_output=$(df -P 2>/dev/null); then
    disk_lines=$(awk '
        NR > 1 && $1 != "tmpfs" && $1 != "overlay" {
            printf "%s\t%s\t%s\n", $1, $5, $NF
        }
    ' <<<"$disk_output")

    if [[ -n $disk_lines ]]; then
        while IFS=$'\t' read -r filesystem percent mountpoint; do
            [[ -z $filesystem ]] && continue
            numeric_percent=${percent%\%}
            if [[ $numeric_percent =~ ^[0-9]+([.][0-9]+)?$ ]]; then
                record "Disk $mountpoint ($filesystem)" "$percent used" \
                    "$(status_for_percent "$numeric_percent")"
            else
                record "Disk $mountpoint ($filesystem)" "unavailable" "CRIT"
            fi
        done <<<"$disk_lines"
    else
        record "Disk" "no eligible filesystems" "CRIT"
    fi
else
    record "Disk" "unavailable" "CRIT"
fi

for service in nginx docker cron; do
    if service_state=$(systemctl is-active "$service" 2>/dev/null) &&
        [[ $service_state == "active" ]]; then
        service_status=OK
    else
        service_status=CRIT
        service_state=${service_state:-unknown}
    fi
    record "Service $service" "$service_state" "$service_status"
done

printf -v check_rule '%*s' "$check_width" ''
printf -v value_rule '%*s' "$value_width" ''
check_rule=${check_rule// /-}
value_rule=${value_rule// /-}
printf '%-*s | %-*s | %s\n' "$check_width" "CHECK" "$value_width" "VALUE" "STATUS"
printf '%s-+-%s-+-%s\n' "$check_rule" "$value_rule" "------"
for index in "${!checks[@]}"; do
    printf '%-*s | %-*s | %s\n' \
        "$check_width" "${checks[$index]}" \
        "$value_width" "${values[$index]}" \
        "${statuses[$index]}"
done

case "$overall" in
    0) overall_text=OK ;;
    1) overall_text=WARN ;;
    *) overall_text=CRIT ;;
esac

printf '\nOVERALL: %s\n' "$overall_text"
exit "$overall"
