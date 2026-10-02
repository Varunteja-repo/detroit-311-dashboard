# Reference numbers

Computed by `scripts/prepare_data.py` from the City's feature service on October 1, 2026 (requests created in 2025, UTC). Both dashboards should reproduce these; small drifts are normal because the City updates records as requests close.

## KPI cards

| Measure | All requests (Is Internal = All) | Resident requests (Is Internal = False) |
|---|---|---|
| Total Requests | 93,981 | 68,897 |
| Closed Requests | 91,172 | 66,558 |
| Closure Rate | 97.0% | 96.6% |
| Median Days to Close | 5.0 | 5.0 |
| % Closed Over 30 Days | 7.8% | 7.1% |
| Median Days to Ack | 0.0 | 0.0 |

## By month (all requests)

| Month | Requests | Closed | Median days to close | Avg days to close |
|---|---|---|---|---|
| Jan | 7273 | 7158 | 3.0 | 11.1 |
| Feb | 5710 | 5536 | 4.0 | 15.8 |
| Mar | 7561 | 7412 | 4.0 | 12.1 |
| Apr | 9130 | 8939 | 4.0 | 11.7 |
| May | 10531 | 10213 | 5.0 | 12.2 |
| Jun | 10009 | 9577 | 7.0 | 11.7 |
| Jul | 11064 | 10718 | 7.0 | 14.2 |
| Aug | 9542 | 9138 | 9.0 | 14.9 |
| Sep | 7626 | 7305 | 8.0 | 11.9 |
| Oct | 6868 | 6691 | 7.0 | 11.3 |
| Nov | 4416 | 4305 | 5.0 | 10.2 |
| Dec | 4251 | 4180 | 3.0 | 7.5 |

## Top 10 request types (all requests)

| Request type | Requests | Closed | Median days to close | Avg days to close |
|---|---|---|---|---|
| DPW - Other environmental - DPW USE ONLY | 9475 | 9390 | 0.0 | 1.7 |
| DPW - Debris Removal - DPW USE ONLY | 8927 | 8908 | 21.0 | 29.5 |
| Tall Grass and Weeds | 8023 | 7531 | 10.0 | 10.2 |
| Request Recycling Cart | 7180 | 7064 | 10.0 | 19.0 |
| Illegal Dump Sites | 6609 | 6066 | 8.0 | 8.3 |
| Curbside - DPW ONLY | 5758 | 5634 | 5.0 | 5.2 |
| Curbside Solid Waste Issue | 4798 | 4407 | 7.0 | 7.8 |
| Abandoned Vehicle - On Street | 4768 | 4675 | 2.0 | 3.7 |
| Water In Basement Investigation | 3741 | 3736 | 2.0 | 6.2 |
| Investigate Water Main Break | 3621 | 3507 | 1.0 | 4.6 |

## Council districts (all requests)

| District | Requests | Closed | Median days to close | Avg days to close |
|---|---|---|---|---|
| District 1 | 13329 | 12949 | 6.0 | 11.4 |
| District 3 | 13650 | 13257 | 6.0 | 12.6 |
| District 5 | 11658 | 11204 | 6.0 | 13.5 |
| District 7 | 14423 | 14088 | 6.0 | 11.3 |
| District 2 | 12023 | 11694 | 5.0 | 12.0 |
| District 4 | 14206 | 13706 | 5.0 | 13.5 |
| District 6 | 9755 | 9480 | 5.0 | 12.9 |
| Unassigned | 4937 | 4794 | 2.0 | 10.7 |

## Top 10 request types (Is Internal = False)

| Request type | Requests | Closed | Median days to close | Avg days to close |
|---|---|---|---|---|
| Tall Grass and Weeds | 8023 | 7531 | 10.0 | 10.2 |
| Request Recycling Cart | 7180 | 7064 | 10.0 | 19.0 |
| Illegal Dump Sites | 6609 | 6066 | 8.0 | 8.3 |
| Curbside Solid Waste Issue | 4798 | 4407 | 7.0 | 7.8 |
| Abandoned Vehicle - On Street | 4768 | 4675 | 2.0 | 3.7 |
| Water In Basement Investigation | 3741 | 3736 | 2.0 | 6.2 |
| Investigate Water Main Break | 3621 | 3507 | 1.0 | 4.6 |
| Tree Issue | 3116 | 3113 | 2.0 | 8.1 |
| Abandoned Vehicles – On private property | 2905 | 2871 | 3.0 | 5.1 |
| DPW DR Coordinator | 2604 | 2541 | 10.0 | 32.4 |

## Council districts (Is Internal = False)

| District | Requests | Closed | Median days to close | Avg days to close |
|---|---|---|---|---|
| District 3 | 9750 | 9451 | 6.0 | 12.3 |
| District 7 | 9115 | 8834 | 6.0 | 11.5 |
| District 1 | 9433 | 9100 | 5.0 | 11.0 |
| District 2 | 8629 | 8347 | 5.0 | 12.4 |
| District 4 | 10605 | 10207 | 5.0 | 13.0 |
| District 5 | 8659 | 8287 | 5.0 | 12.8 |
| District 6 | 7981 | 7739 | 4.0 | 12.0 |
| Unassigned | 4725 | 4593 | 2.0 | 9.2 |

## Channel

| Report method | Requests | Share |
|---|---|---|
| direct | 93515 | 99.5% |
| phone | 213 | 0.2% |
| public_meeting | 120 | 0.1% |
| walkin | 92 | 0.1% |
| internal | 19 | 0.0% |
| email | 18 | 0.0% |
| other | 4 | 0.0% |

## Data quality

| Check | Requests |
|---|---|
| No council district | 4,937 (5.3%) |
| Internal requests (request type contains ONLY) | 25,084 |
| Outside the Detroit map bounds or missing coordinates | 8,580 |
| Closed but no num_days_to_close | 0 |
| Open but has num_days_to_close | 0 |
