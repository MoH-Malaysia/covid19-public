# Documentation for epidemic datasets

## File naming convention

| Filename | Naming convention | Update frequency |
| :--- | :---: | :---: |
| cases_malaysia.csv | Static name | Daily by 2359 (for T-0) |
| cases_state.csv | Static name | Daily by 2359 (for T-0) |
| deaths_malaysia.csv | Static name | Daily by 2359 (for T-0) |
| deaths_state.csv | Static name | Daily by 2359 (for T-0) |
| clusters.csv | Static name | Daily by 2359 (for T-1) |
| pkrc.csv| Static name |  Daily by 2359 (for T-0) |
| hospital.csv | Static name |  Daily by 2359 (for T-0) |
| icu.csv | Static name |  Daily by 2359 (for T-0) |
| tests_malaysia.csv | Static name | At least twice weekly |
| tests_state.csv | Static name | At least twice weekly |

## Variables and Methodology

### Cases and Testing

1) `date`: yyyy-mm-dd format; data correct as of 1200hrs on that date
2) `state`: name of state (present in state file, but not country file)
3) `cases_new`: cases reported in the 24h since the last report
4) `cases_import`: imported cases reported in the 24h since the last report
5) `cases_active`: Covid+ individuals who have not recovered or died
6) `cases_recovered` recovered cases reported in the 24h since the last report
7) `cases_cluster`: number of cases attributable to clusters; the difference between `cases_new` and the sum of cases attributable to clusters is the number of sporadic cases
8) `cluster_x`: cases attributable to clusters under category `x`; possible values for `x` are import, religious, community, highRisk, education, detentionCentre, and workplace
9) `cases_agecat`: cases falling into one of 4 age categories, i.e. child (0-11), adolescent (12-17), adult (18-59), elderly (60+); note that the sum of cases by age may not equal the total cases for that day, as some cases are registered without ages or with unverifiable age data 
10) `cases_pvax`: number of partially-vaccinated individuals who tested positive for Covid (perfect subset of `cases_new`), where "partially vaccinated" is defined as receiving at least 1 dose of a 2-dose vaccine at least 1 day prior to testing positive, or receiving the Cansino vaccine between 1-27 days before testing positive
11) `cases_fvax`: number of fully-vaccinated who tested positive for Covid (perfect subset of `cases_new`), where "fully vaccinated" is defined as receiving the 2nd dose of a 2-dose vaccine at least 14 days prior to testing positive, or receiving the Cansino vaccine at least 28 days before testing positive
12) `rtk-ag`: number of tests done using Antigen Rapid Test Kits (RTK-Ag)
13) `pcr`: number of tests done using Real-time Reverse Transcription Polymerase Chain Reaction (RT-PCR) technology

### Deaths

1) `date`: yyyy-mm-dd format; data correct as of 1200hrs on that date
2) `state`: name of state (present in state file, but not country file)
3) `deaths_new`: deaths due to COVID-19 based on **date reported to public**
4) `deaths_bid`: deaths due to COVID-19 which were brought-in dead based on **date reported to public** (perfect subset of `deaths_new`)
5) `deaths_new_dod`: deaths due to COVID-19 based on **date of death**
6) `deaths_bid_dod`: deaths due to COVID-19 which were brought-in dead based on **date of death** (perfect subset of `deaths_new_dod`)
7) `deaths_pvax`: number of partially-vaccinated individuals who died due to COVID-19 based on **date of death** (perfect subset of `deaths_new_dod`), where "partially vaccinated" is defined as receiving at least 1 dose of a 2-dose vaccine at least 1 day prior to testing positive, or receiving the Cansino vaccine between 1-27 days before testing positive.
8) `deaths_fvax`: number of fully-vaccinated who died due to COVID-19 based on **date of death** (perfect subset of `deaths_new_dod`), where "fully vaccinated" is defined as receiving the 2nd dose of a 2-dose vaccine at least 14 days prior to testing positive, or receiving the Cansino vaccine at least 28 days before testing positive.
9) `deaths_tat`: median days between date of death and date of report for all deaths reported on the day

### Cluster analysis

1) `cluster`: unique textual identifier of cluster; nomenclature does not necessarily signify address
2) `state` and `district`: geographical epicentre of cluster, if localised; inter-district and inter-state clusters are possible and present in the dataset
3) `date_announced`: date of declaration as cluster
4) `date_last_onset`: most recent date of onset of symptoms for individuals within the cluster. note that this is distinct from the date on which said individual was tested, and the date on which their test result was received; consequently, today's date may not necessarily be present in this column.
5) `category`: classification as per variable `cluster_x` above
6) `status`: active or ended
7) `cases_new`: number of new cases detected within cluster in the 24h since the last report
8) `cases_total`: total number of cases traced to cluster
9) `cases_active`: active cases within cluster
10) `tests`: number of tests carried out on individuals within the cluster; denominator for computing a cluster's current positivity rate
11) `icu`: number of individuals within the cluster currently under intensive care
12) `deaths`: number of individuals within the cluster who passed away due to COVID-19
13) `recovered`: number of individuals within the cluster who tested positive for and subsequently recovered from COVID-19


### Healthcare 

_The datasets below have been constructed to provide 3 kinds of insight. First, the inflow and outflow of patients from quarantine centres, hospitals, and intensive care is, without any further scaling or context, critical to monitor - especially when clear divergences between infections and healthcare outcomes start to be observed (e.g. due to vaccination). Second, comparing against available capacity (number of beds, intensive care units, ventilators) allows for understanding of the strain exerted by the epidemic on the healthcare system. Third, the inclusion of datapoints on non-Covid patients demonstrates the interactions between the epidemic and broader health outcomes._

### PKRC (COVID-19 Quarantine and Treatment Centre)

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: name of state; note that (unlike with other datasets), it is not necessary that there be an observation for every state on every date. for instance, there are no PKRCs in W.P. Kuala Lumpur and W.P Putrajaya.
3) `beds`: total PKRC beds (with related medical infrastructure)
4) `admitted_x`: number of individuals in category `x` admitted to PKRCs, where `x` can be suspected/probable, COVID-19 positive, or non-COVID
5) `discharged_x`: number of individuals in category `x` discharged from PKRCs
6) `pkrc_x`: total number of individuals in category `x` in PKRCs; this is a stock variable altered by flows from admissions and discharges


### Hospital

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: name of state, with similar qualification on exhaustiveness of date-state combos as PKRC data
3) `beds`: total hospital beds (with related medical infrastructure)
3) `beds_covid`: total beds dedicated for COVID-19
4) `beds_noncrit`: total hospital beds for non-critical care
5) `admitted_x`: number of individuals in category `x` admitted to hospitals, where `x` can be suspected/probable, COVID-19 positive, or non-COVID
6) `discharged_x`: number of individuals in category `x` discharged from hospitals
7) `hosp_x`: total number of individuals in category `x` in hospitals; this is a stock variable altered by flows from admissions and discharges


### ICU

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: name of state, with similar qualification on exhaustiveness of date-state combos as PKRC data
3) `beds_icu`: total gazetted ICU beds
4) `beds_icu_rep`: total beds aside from (3) which are temporarily or permanently designated to be under the care of Anaesthesiology & Critical Care departments
5) `beds_icu_total`: total critical care beds available (with related medical infrastructure)
6) `beds_icu_covid`: total critical care beds dedicated for COVID-19
7) `vent`: total available ventilators
8) `vent_port`: total available portable ventilators
9) `icu_x`: total number of individuals in category `x` under intensive care, where `x` can be  suspected/probable, COVID-19 positive, or non-COVID; this is a stock variable
10) `vent_x`: total number of individuals in category `x` on mechanical ventilation, where `x` can be suspected/probable, COVID-19 positive, or non-COVID; this is a stock variable

