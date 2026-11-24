# Runbook: Restart nginx on a Web Node

| Field | Value |
|---|---|
| Applies to | Ubuntu 22.04 web nodes running nginx |
| Owner group | Linux Operations |
| Risk | Medium |
| Approval needed | Yes (incident commander or Operations lead) |

## 1. Purpose

1. Restore site availability by safely restarting nginx when users report that the site is down.

2. Do not use this runbook for configuration changes or cache deletion.

## 2. Pre-checks (read-only)

1. Confirm that an active incident or approved operational request identifies the affected site and server.

2. Connect to the affected server: `ssh <administrator>@<web-node>`.

3. Confirm the affected server: `hostnamectl --static`.

   Expected output: The documented web node name, for example `web-01`.

4. Check the current nginx service state: `systemctl status nginx --no-pager`.

   Expected output: The service state is shown as `active (running)`, `inactive`, or `failed`. Record the state and any recent error before proceeding.

5. Validate the nginx configuration: `sudo nginx -t`.

   Expected output:

   ```text
   nginx: configuration file /etc/nginx/nginx.conf test is successful
   ```

6. Confirm whether nginx has a listening web port: `sudo ss -ltnp | grep nginx`.

   Expected output: At least one `LISTEN` line for nginx, normally on port `80`, `443`, or the application's documented port. No line is acceptable only if the service is currently failed or inactive.

7. Record the local HTTP status before the restart: `curl -sS -o /dev/null -w '%{http_code}\n' http://localhost`.

   Expected output: The normal documented success code, commonly `200`. A timeout, connection error, or `5xx` status supports the restart decision.

8. Stop this runbook and escalate if the server is not the affected node, `nginx -t` fails, or another operator is changing the server.

## 3. Steps (numbered, one action each, exact command)

1. Obtain approval from the incident commander or Operations lead.

2. Restart nginx: `sudo systemctl restart nginx`.

3. Do not clear the cache during this procedure unless the application team supplies and approves the exact path.

## 4. Verification (command + expected result)

1. Verify the service state: `systemctl status nginx --no-pager`.

   Expected output: `Active: active (running)` with no new failure message.

2. Verify that nginx is listening: `sudo ss -ltnp | grep nginx`.

   Expected output: A `LISTEN` line for the documented web port, normally `80` or `443`.

3. Verify the local site response: `curl -sS -o /dev/null -w '%{http_code}\n' http://localhost`.

   Expected output: The documented success code, commonly `200`, rather than a `5xx` status, timeout, or connection error.

4. Verify the external site response: `curl -sS -o /dev/null -w '%{http_code}\n' https://<site-hostname>`.

   Expected output: The site's normal `2xx` or `3xx` HTTP status.

5. Inspect recent nginx service events: `sudo journalctl -u nginx --since '10 minutes ago' --no-pager`.

   Expected output: Normal stop/start messages and no configuration, permission, port-binding, or worker failure errors.

6. Record the execution time, service state, HTTP status, and outcome in the incident or change record.

## 5. Rollback

1. Note that the runbook changes only service state and does not modify nginx configuration.

2. If nginx is not running after the restart, validate the configuration: `sudo nginx -t`.

   Expected output: `nginx: configuration file /etc/nginx/nginx.conf test is successful`.

3. If the configuration test succeeds, start nginx: `sudo systemctl start nginx`.

4. Verify the rollback service state: `systemctl status nginx --no-pager`.

   Expected output: `Active: active (running)`.

5. Verify the rollback HTTP response: `curl -sS -o /dev/null -w '%{http_code}\n' http://localhost`.

   Expected output: The documented success code, commonly `200`.

6. Stop further restart attempts and escalate if configuration validation fails or nginx remains unavailable.

## 6. Escalate when

1. Escalate to Linux Operations L2 immediately if `sudo nginx -t` reports a configuration error.

2. Escalate to Linux Operations L2 if nginx remains `inactive` or `failed` after one restart and one start attempt.

3. Escalate to the application team if nginx is active and listening but the site still times out, returns `5xx`, or returns unexpected content.

4. Escalate to the incident commander if multiple web nodes are affected or if availability worsens after the restart.

5. Contact the application team before clearing any cache. Do not guess or delete a cache path.

## 7. Change history

1. 2026-11-23 — Converted SOP-OPS-014 into the standard runbook format and added pre-checks, verification, rollback, and escalation criteria.
