# Runbook: Disk Space Low

| Field | Value |
|---|---|
| Applies to | Linux hosts with the `DiskSpaceLow` alert active on `/var` |
| Owner group | LINUX-L2 |
| Risk | High |
| Approval needed | Yes, before compression, deletion, service restart, or resize |

## 1. Purpose

1. Identify the source of disk growth and recover free space without deleting evidence or data that has not been approved for removal.

## 2. Pre-checks (read-only)

1. Confirm the affected alert instance and mount point in Prometheus.
2. Check overall usage and inodes: `df -h /var; df -i /var`.
3. Identify the largest directories: `sudo du -x -h --max-depth=2 /var 2>/dev/null | sort -h | tail -20`.
4. Identify large files: `sudo find /var -xdev -type f -size +100M -printf '%s %p\n' 2>/dev/null | sort -n | tail -20`.
5. Check deleted files still held open: `sudo lsof +L1 2>/dev/null | grep -E '/var|deleted'`.
6. Check log rotation configuration and recent service errors.
7. Stop if the mount is not the affected file system, if the files are unfamiliar, or if active database data occupies the space.

## 3. Steps (numbered, one action each, exact command)

1. Obtain approval identifying the exact safe directory and retention period.
2. Compress an approved inactive log pattern: `sudo find <approved-log-directory> -name '*.log' -mtime +<retention-days> -exec gzip {} \;`.
3. If a process holds a deleted log open, obtain service-owner approval before restarting that documented service: `sudo systemctl restart <service>`.
4. Record the affected path, reclaimed bytes, approval, and incident timestamp.

## 4. Verification (command + expected result)

1. Verify free space: `df -h /var`.

   Expected output: Free space increases and usage falls below the alert threshold with operational headroom.

2. Verify inode use: `df -i /var`.

   Expected output: Inode use remains below the critical operational threshold.

3. Verify affected services remain healthy using their documented health check.
4. Verify the `DiskSpaceLow` alert resolves after the next Prometheus evaluation.

## 5. Rollback

1. Do not delete backup archives created during this procedure.
2. If compression causes an application to fail, stop further file operations and restore the original approved file from the available backup.
3. Restart only the approved affected service if required to return to service.
4. Roll back must preserve the original ownership, permissions, and file contents.

## 6. Escalate when

1. Escalate immediately when the file system is at 100%, inode use is exhausted, or writes are failing.
2. Escalate to the application or database owner before touching unknown application data.
3. Escalate to LINUX-L2 for recurring growth, an undersized volume, or growth that returns within 24 hours.
4. Escalate to the infrastructure owner for an approved volume resize or storage change.
5. Escalate to SECOPS if unexpected files or unexplained data growth are found.

## 7. Change history

1. 2026-11-25 - Created from the `DiskSpaceLow` alert troubleshooting checklist.

