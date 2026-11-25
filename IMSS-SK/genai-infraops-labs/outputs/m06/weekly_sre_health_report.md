# Weekly SRE Health Report

**Reporting period:** 2026-11-01 to 2026-11-07  
**Source:** `data/metrics/metrics_export.csv` (21 service-day records)  
**Reference SLO:** 99.5% availability, from the Module 6 lab definition

## Executive summary

1. **Customer Portal is the highest acute risk.** On 2026-11-05 it fell to **98.10% availability**, with **3,106 ms p95 latency** and **4.72% errors**. Four incidents were recorded during the week.
2. **Finance Reporting is the highest sustained SLO risk.** Its weekly average availability was **99.394%**, below the 99.5% reference SLO on average. Availability dipped to **99.33%** on 2026-11-04, and p95 latency ended the week at its weekly peak of **851 ms**.
3. **Email remained healthiest on availability.** Its weekly average availability was **99.836%**, although it recorded four incidents and ended with a **0.56% error rate**, its weekly peak.

## Weekly service scorecard

| Service | Avg availability | Avg p95 latency | Avg error rate | Avg CPU | Incidents | Reference SLO |
|---|---:|---:|---:|---:|---:|---|
| Customer Portal | 99.569% | 887.9 ms | 1.034% | 56.4% | 4 | Met overall, with one major daily breach |
| Finance Reporting | 99.394% | 622.4 ms | 0.349% | 58.7% | 1 | Missed by 0.106 percentage points |
| Email | 99.836% | 603.4 ms | 0.367% | 55.9% | 4 | Met overall |

## Top risks

### 1. Customer Portal incident on November 5

- Availability dropped from 99.86% on November 4 to **98.10%** on November 5.
- P95 latency increased from 556 ms to **3,106 ms**.
- Errors increased from 0.30% to **4.72%**.
- CPU increased from 48% to 72%, while one incident was recorded.
- **Risk:** A recurrence could exhaust the weekly availability error budget and materially disrupt customer access.
- **Assessment:** The metrics show acute degradation, but they do not prove CPU as the root cause.

### 2. Finance Reporting below the reference SLO

- Weekly average availability was **99.394%** versus a 99.5% reference SLO.
- The service missed the reference SLO on all seven days; November 7 was its best result at 99.48%, still 0.02 percentage points below 99.5%.
- CPU peaked at **69%** on November 4, alongside 99.33% availability and a 0.71% error rate.
- P95 latency reached **851 ms** on November 7, a **21.4% increase** from 701 ms on November 1.
- **Risk:** Continued small availability and latency breaches can accumulate into a reliability problem even without a high incident count.

### 3. Email incidents despite healthy availability

- Weekly average availability was **99.836%**, but the service recorded **four incidents**.
- P95 latency ranged from 402 ms to **897 ms**.
- The error rate ended at **0.56%** on November 7, its weekly peak.
- **Risk:** Availability can mask user-impacting intermittent failures, delivery delays, or mailbox-specific errors.

## Trends

| Trend | Evidence | Interpretation |
|---|---|---|
| Portal recovered after a severe midweek event | 98.10% availability and 3,106 ms p95 on Nov 5; 99.81% and 498 ms on Nov 6 | Recovery was fast, but recurrence prevention is still required. |
| Finance latency rose into week-end | 701 ms on Nov 1; 851 ms on Nov 7 | Investigate query, dependency, and capacity trends despite lower end-of-week errors. |
| Email errors worsened while CPU fell | 0.03% errors and 62% CPU on Nov 1; 0.56% errors and 38% CPU on Nov 7 | Errors are not explained by average CPU alone; application or dependency checks are warranted. |
| Incident counts were concentrated | Customer Portal: 4; Email: 4; Finance Reporting: 1 | Portal and Email require more recurrence reduction work than their weekly averages alone suggest. |

## Reference error-budget view

At a 99.5% weekly availability target, the error budget is 0.5%, equivalent to **50.4 minutes** over seven days.

| Service | Average unavailability | Approx. weekly downtime | Error-budget use |
|---|---:|---:|---:|
| Customer Portal | 0.431% | 43.5 minutes | 86.2% |
| Finance Reporting | 0.606% | 61.0 minutes | 121.0% |
| Email | 0.164% | 16.5 minutes | 32.8% |

Finance Reporting consumed more than its reference error budget. The calculation uses daily percentage averages as equally weighted service-day samples because request volume is not present in the export.

## Recommended actions

1. **P1 - Review the Customer Portal November 5 incident.** Correlate application, NGINX, dependency, saturation, deployment, and 5xx timelines around 3106 ms p95 latency and 4.72% errors. Assign to APP-PORTAL-L2 with LINUX-L2 support.
2. **P1 - Create a Finance Reporting reliability action.** Investigate why availability missed 99.5% on six of seven days and why p95 latency reached 851 ms. Assign to LINUX-L2 and include database-query owners.
3. **P2 - Add or verify service-level alerting.** Alert on availability error-budget burn, p95 latency, and error-rate thresholds rather than CPU alone.
4. **P2 - Review Email incident recurrence.** Link all four incidents to release, dependency, mail-routing, and error-code evidence and determine why average availability is healthy while incidents persist.
5. **P2 - Improve next week's data.** Add request count, error status counts, deployment markers, and per-component SLI data so weighted availability and causal attribution can be calculated.

## Monitoring limitations

- The CSV contains one aggregate record per service per day, not raw requests or time-series samples.
- No documented per-service SLO file is present; 99.5% is used as the lab reference target.
- Error-budget downtime is an approximation because traffic weighting and the exact measurement window are unavailable.
- Incident records have not been linked to this export, so this report does not claim a causal link between concurrent metrics and incidents.
