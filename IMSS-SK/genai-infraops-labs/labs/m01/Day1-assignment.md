# Disk-Full Incident Troubleshooting Checklist

| Step | Command | Why | Expected result |
|---:|---|---|---|
| 1 | `df -h /var` | Confirm current capacity on the filesystem identified by the alert. | `/var` usage is confirmed at or near 96%, or current recovery is shown. |
| 2 | `df -i /var` | Check for inode exhaustion as another cause of write failures. | Inode usage and available inodes are reported. |
| 3 | `systemctl status finapp` | Verify service health and the reported `No space left on device` error. | `finapp` status and relevant recent messages are displayed. |
| 4 | `journalctl -u finapp --since "2026-11-09 07:00:00"` | Review service activity from shortly after it started. | Evidence confirms or rules out ongoing write failures. |
| 5 | `sudo du -xh /var --max-depth=2 \| sort -h \| tail -15` | Locate the largest consumers under `/var` without modifying files. | A ranked, read-only list identifies the highest-usage directories. |
| 6 | `sudo stat /var/log/finapp/report.log` | Inspect the exact log file named by `finapp`. | Size, ownership, and timestamps indicate whether this file is a likely contributor. |
| 7 | `sudo lsof +L1 /var` | Detect deleted files still held open and consuming capacity. | Deleted-but-open files and owning processes are listed, or none are found. |
| 8 | `sudo du -ah /var \| sort -h \| tail -30` | Produce a detailed list of candidate files for review. | Full paths and sizes are available; nothing is changed. |
| 9 | No cleanup command. List every candidate's full path, size, age, owner, and proposed action, then request approval from `LINUX-L2` or the incident authority. | Prevent unauthorized deletion and retain ITIL audit evidence. | Written approval identifies exactly which files may be changed and how. |
| 10 | **ASSUMPTION:** The approved plan may require reopening or restarting `finapp` if a deleted file is held open. Perform only the approved action. | Release space retained by an open deleted file without deleting unrelated data. | The process releases the consumed space and remains healthy. |
| 11 | `df -h /var` | Verify that approved remediation recovered capacity. | `/var` has adequate free space and usage is below the agreed threshold. |
| 12 | `systemctl status finapp` | Verify service recovery. | `finapp` is active and no disk-full failure is reported. |
| 13 | `journalctl -u finapp --since "5 minutes ago"` | Check for recurring write errors after remediation. | No new `No space left on device` messages appear; otherwise escalate. |

No files are deleted without listing them and obtaining explicit approval.
