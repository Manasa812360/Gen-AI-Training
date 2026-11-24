# Disk-full incident checklist

## Safer troubleshooting checklist

| Step | Command | Why | Expected result |
|---:|---|---|---|
| 1 | `df -h /var` | Confirm current usage of the `/var` filesystem. | Usage is below 96% if space recovered, or remains at or above the critical threshold. |
| 2 | `df -i /var` | Rule out inode exhaustion as a possible cause. | Inode usage and available inodes are shown. |
| 3 | `systemctl status finapp` | Check whether the application is healthy and still reporting write failures. | Service state is displayed with the latest relevant status. |
| 4 | `journalctl -u finapp --since "2026-11-09 07:00:00"` | Review service logs around the incident. | Confirmation or additional evidence of `No space left on device` errors. |
| 5 | `sudo du -xh /var --max-depth=2 \| sort -h \| tail -15` | Identify the largest `/var` directories without changing data. | A ranked list of directory usage within `/var`. |
| 6 | `sudo stat /var/log/finapp/report.log` | Verify the log file reported by `finapp` and measure it. | File size and timestamps are displayed. |
| 7 | `sudo lsof +L1 /var` | Find deleted files under `/var` that remain open and continue consuming space. | Any deleted, open files are listed with the owning process. |
| 8 | Prepare an exact list of candidate files, including full paths and sizes. Use no cleanup command. | Ensure that any proposed cleanup is safe and reviewable. | A reviewed candidate list with no files removed. |
| 9 | Obtain approval from `LINUX-L2` or the incident authority before cleanup. | Prevent unapproved deletion and maintain ITIL change control. | Approval is recorded, or cleanup is stopped. |
| 10 | **ASSUMPTION:** After approval, compressing old files instead of deleting them is acceptable under the incident policy. | Preserve historical data while recovering space. | No deletion occurs unless separately approved. |
| 11 | `df -h /var` | Verify recovery after approved remediation. | `/var` is below the target threshold, or the result is escalated. |
| 12 | `systemctl status finapp` | Confirm application recovery and renewed write activity. | `finapp` is running and no new disk-full write errors are present. |

## Comparison notes

- The second answer is safer because cleanup is conditional on explicit approval.
- Neither answer offered `rm -rf` or another deletion command.
- Neither answer invented a hostname or used a path absent from the scenario.
- The `lsof +L1 /var` check is potentially a privileged read-only check; sudo is required to inspect all processes and open files.
- The first answer's more specific log-rotation assumption is not confirmed by the scenario and should not be treated as fact.
