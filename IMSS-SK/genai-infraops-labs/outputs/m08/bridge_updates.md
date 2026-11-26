# Major Incident Stakeholder Updates — INC-MAJ-0042

## As at 18:51 IST

**Status:** Identified  
**Customer impact:** Customers are unable to log in to the Customer Portal. All login requests use the affected code path, and no workaround is currently available.  
**What we know:** Portal API 2.4.0 was deployed at 18:05 with a database migration. Login requests have returned errors since approximately 18:07. The database is healthy with no locks. Investigation found that the `last_login_ts` column is missing because migration step 3 failed while the deployment pipeline reported success.  
**Actions in progress:** Application team — determine the corrective action for the failed migration.  
**Decisions taken:** No recovery decision has been recorded yet.  
**Next update at:** 19:21 IST.

**Customer-safe status-page version:** We are investigating a service issue affecting Customer Portal login. We have identified a failed deployment step and are determining the safest corrective action; the next update will be at 19:21 IST.

## As at 19:21 IST

**Status:** Mitigating  
**Customer impact:** Customers remain unable to log in to the Customer Portal. All login requests use the affected code path, and no workaround is currently available.  
**What we know:** Portal API 2.4.0 was deployed at 18:05 with a database migration. Migration step 3 failed to create the required `last_login_ts` column, although the deployment pipeline reported success. The database is healthy.  
**Actions in progress:** Platform team — roll back the portal API to version 2.3.7.  
**Decisions taken:** The Major Incident team approved rollback to 2.3.7 through emergency change ECHG0003049.  
**Next update at:** 19:51 IST.

**Customer-safe status-page version:** We have identified the cause of the Customer Portal login issue and approved a rollback to the previous stable service version. The rollback is in progress, and the next update will be at 19:51 IST.

## As at 19:51 IST

**Status:** Mitigating  
**Customer impact:** Customers remain unable to log in to the Customer Portal. All login requests use the affected code path, and no workaround is currently available.  
**What we know:** The failed migration in portal API 2.4.0 left a required database column missing. Rollback to 2.3.7 was approved, but the previous image was no longer available in the registry because of the retention policy.  
**Actions in progress:** Platform team — rebuild version 2.3.7 from its Git tag and deploy it.  
**Decisions taken:** Continue with the approved rollback to version 2.3.7 after rebuilding the removed image.  
**Next update at:** 20:21 IST.

**Customer-safe status-page version:** The approved rollback is delayed while the previous Customer Portal version is rebuilt. The service remains unavailable for login, and the next update will be at 20:21 IST.
