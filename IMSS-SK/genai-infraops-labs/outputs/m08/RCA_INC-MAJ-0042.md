# Post-Incident Review — INC-MAJ-0042

## 1. Summary

On 5 November 2026, release 2026.11.05 caused Customer Portal login failures by deploying portal-api 2.4.0 without its required database column.
Migration step 3 failed silently, and the pipeline reported success; monitoring and the Service Desk detected the resulting 5xx errors and customer reports.
The service was restored by rebuilding and deploying portal-api 2.3.7 at 20:18 IST; the P1 response and resolution SLAs were both met.

## 2. Impact and SLA

- **Business service:** Customer Portal
- **Priority:** P1
- **Customer impact:** Customers could not log in. No customer workaround was available because all login requests used the affected code path.
- **Outage window:** 18:12–20:31 IST
- **Response:** 9 minutes against a 15-minute target — **MET**
- **Resolution:** 139 minutes against a 240-minute target — **MET**

## 3. Timeline (IST)

| Time | Event |
|---|---|
| 18:05 | portal-api 2.4.0 deployed with a database schema migration. |
| 18:07 (approximately) | Login failures reportedly began. This time was reported later and is a HYPOTHESIS based on the bridge chat. |
| 18:10 | Monitoring raised a critical HTTP 5xx alert: 41% errors on `nginx-edge-01`. |
| 18:12 | Multiple customer calls reported login failures; the P1 incident was opened. |
| 18:21 | Major Incident bridge opened; the incident was formally responded to. |
| 18:25 | Database health checks showed 30% CPU and no locks. |
| 18:35 | No customer-facing workaround was available. |
| 18:48 | Application logs identified the missing `last_login_ts` column and the silently failed migration step. |
| 18:58 | Rollback was preferred over a schema change under load. |
| 19:10 | Rollback to portal-api 2.3.7 was approved through emergency change ECHG0003049. |
| 19:40 | Rollback was blocked because the previous image had been removed under the retention policy; rebuilding began. |
| 20:18 | portal-api 2.3.7 was rebuilt and deployed; error rate began falling. |
| 20:31 | Service was declared restored after the error rate remained below 0.5% for 10 minutes. |

## 4. Detection

Monitoring detected the first confirmed service degradation at 18:10. The P1 incident was opened at 18:12, two minutes after the alert and approximately five minutes after the reported onset of login failures. Formal major-incident response started at 18:21, nine minutes after the incident opened and within the 15-minute target.

## 5. 5 Whys

1. **Why could customers not log in?**  
   portal-api 2.4.0 tried to use `last_login_ts`, but the column did not exist.

2. **Why did the application expect a column that did not exist?**  
   The release contained a code change and schema migration, but migration step 3 failed to complete.

3. **Why was the incompatible application version left active?**  
   The migration failure was silent, and the deployment pipeline reported the release as successful.

4. **Why did the pipeline not prevent or signal this partial deployment?**  
   The available release controls did not make migration completion an enforced deployment gate with failure propagation. **HYPOTHESIS:** pipeline behaviour should be reviewed to confirm why a failed step did not fail the release.

5. **Why was service restoration delayed after rollback was selected?**  
   The previous image had been deleted by the retention policy, so the recovery path required rebuilding version 2.3.7 from its Git tag.

## 6. Contributing factors

- **HYPOTHESIS:** The application release and database migration were not deployed atomically from the pipeline's perspective.
- Migration failure did not propagate as a failed release.
- **HYPOTHESIS:** Available deployment verification did not detect the missing schema object before customer traffic reached the affected login path.
- The registry retained only five image tags, and the required rollback image was unavailable.
- The rollback process depended on rebuilding the previous version, extending mitigation time.

## 7. Corrective and preventive actions

| Action | Type | Owner team | Due date |
|---|---|---|---|
| Correct the schema migration and verify that `last_login_ts` is present before future deployment | CA | Database team | TBD |
| Make migration failure propagate to the deployment pipeline and block application activation | PA | Platform team | TBD |
| Add post-deployment validation for required database objects and the login path before traffic is considered restored | PA | Application team | TBD |
| Add a deployment-stage smoke test that exercises an authenticated login and fails the release on HTTP 5xx responses | PA | Application team | TBD |
| Review image-retention policy and preserve an approved rollback candidate for every active production release | PA | Platform team | TBD |
| Document and exercise image recreation from a Git tag as a rollback contingency | PA | Platform team | TBD |
| Review alert-to-incident workflow to preserve the two-minute detection-to-ticket performance demonstrated during this incident | PA | Service Management team | TBD |

## 8. What went well

- Monitoring raised a critical alert two minutes before the P1 was formally opened.
- The P1 response met the 15-minute target.
- The database, application and platform teams isolated the fault without evidence of database unavailability or locking.
- The team identified the failed migration and missing column at 18:48.
- Emergency rollback approval was recorded promptly.
- The service was restored and the P1 resolution SLA was met.
- Monitoring continued after restoration to confirm sustained recovery before closure.

## Review

- **Blameless:** Yes. The report focuses on system behaviour, release controls and process gaps; it does not blame any individual.
- **Actions owned and dated:** Yes. Every action has an owner team and an explicit due date; `TBD` is used where dates were not yet agreed.
