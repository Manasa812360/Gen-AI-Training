#!/usr/bin/env bash
# shellcheck disable=SC2317 # Functions are invoked indirectly by the EXIT trap.

set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_DIR
ROOT_DIR="$(cd -- "${SCRIPT_DIR}/../.." && pwd)"
readonly ROOT_DIR
readonly AUDIT_LOG="${ROOT_DIR}/approvals/audit.log"
readonly ALLOWED_SERVICES=("nginx" "cron" "docker")

service="${1:-}"
execute=false
result="failure"
audit_written=false

audit() {
    if [[ "${audit_written}" == true ]]; then
        return
    fi

    mkdir -p -- "$(dirname -- "${AUDIT_LOG}")"
    printf 'time=%s user=%s service=%s result=%s\n' \
        "$(date --iso-8601=seconds)" \
        "${USER:-$(id -un)}" \
        "${service}" \
        "${result}" >> "${AUDIT_LOG}"
    audit_written=true
}

on_exit() {
    local exit_status=$?
    trap - EXIT
    audit
    exit "${exit_status}"
}
trap on_exit EXIT

usage() {
    printf 'Usage: %s <nginx|cron|docker> [--execute]\n' "$(basename -- "$0")" >&2
}

if [[ "$#" -lt 1 || "$#" -gt 2 ]]; then
    usage
    service="<invalid>"
    result="rejected"
    exit 2
fi

case "${service}" in
    nginx|cron|docker) ;;
    *)
        printf 'Error: unsupported service %q. Allowed services: %s\n' \
            "${service}" "${ALLOWED_SERVICES[*]}" >&2
        service="<invalid>"
        result="rejected"
        exit 2
        ;;
esac

if [[ "$#" -eq 2 ]]; then
    if [[ "$2" != "--execute" ]]; then
        printf 'Error: unsupported option %q.\n' "$2" >&2
        usage
        result="rejected"
        exit 2
    fi
    execute=true
fi

printf 'Service: %s\n' "${service}"

if [[ "${execute}" == false ]]; then
    printf 'DRY RUN - no changes will be made.\n'
    printf 'Pre-check: systemctl is-active %q\n' "${service}"
    printf 'Pre-check: journalctl --unit %q --lines 20 --no-pager\n' "${service}"
    printf 'WOULD RUN: sudo systemctl restart %q\n' "${service}"
    printf 'Post-check: systemctl is-active %q\n' "${service}"
    result="dry-run"
    exit 0
fi

printf 'Pre-check status:\n'
if systemctl is-active "${service}"; then
    :
else
    printf 'Warning: %s is not currently active.\n' "${service}" >&2
fi

printf 'Last 20 journal lines for %s:\n' "${service}"
journalctl --unit "${service}" --lines 20 --no-pager

confirmation=""
read -r -p "Type '${service}' to confirm the restart: " confirmation
if [[ "${confirmation}" != "${service}" ]]; then
    printf 'Confirmation did not match. Restart cancelled.\n' >&2
    result="cancelled"
    exit 1
fi

printf 'Restarting %s...\n' "${service}"
sudo systemctl restart "${service}"

printf 'Post-check status:\n'
if systemctl is-active "${service}"; then
    result="success"
    printf '%s restart completed successfully.\n' "${service}"
    exit 0
fi

result="post-check-failed"
printf 'Error: %s is not active after restart.\n' "${service}" >&2
exit 1
