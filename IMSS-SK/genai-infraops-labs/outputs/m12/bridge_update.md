# Bridge update - draft, not published

- **Impact:** Multiple reports of portal login failures and slow reporting;
  actual affected population and severity require desk lead confirmation.
- **Incident timeline:** Release reported at 14:00 IST on 2026-11-12; the
  first supplied portal 5xx alert fired at 14:03. Eighteen portal alerts are
  proposed for one parent; two Finance alerts remain separate.
- **Current lab investigation:** API image pull fails; the web Service
  currently has endpoints. The lab cluster was created after the incident
  date, so these observations do not establish historical cause.
- **Action:** APP-PORTAL-L2 and K8S-PLATFORM-L3 to confirm the intended image,
  ingress host and verification route. No capstone fix has been approved or
  executed.
- **Next update:** Communicator to agree and announce a time with the incident
  lead; no ETA for recovery is confirmed.
