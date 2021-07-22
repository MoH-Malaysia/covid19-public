# Documentation for epidemic datasets

## File naming convention

1) `cases_malaysia.csv`: Static name; file is updated by 2359hrs daily
2) `cases_state.csv`: Static name; file is updated by 2359hrs daily
3) `tests_malaysia.csv`: Static name; file is updated by 2359hrs daily
4) `clusters.csv`: Static name; file is updated by 2359hrs daily
5) `deaths_malaysia.csv`: Static name; file is updated by 2359hrs daily
6) `deaths_state.csv`: Static name; file is updated by 2359hrs daily
7) `pkrc.csv`: Static name; file is updated at least twice weekly
8) `hospital.csv`: Static name; file is updated at least twice weekly
9) `icu.csv`: Static name; file is updated at least twice weekly

## Variables and Methodology

### Cases and Testing

1) `date`: yyyy-mm-dd format; data correct as of 1200hrs on that date
2) `state`: name of state (present in state file, but not country file)
3) `cases_new`: cases reported in the 24h since the last report
4) `cluster_x`: cases attributable to clusters under category `x`; possible values for `x` are import, religious, community, highRisk, education, detentionCentre, and workplace; the difference between `cases_new` and the sum of cases attributable to clusters is the number of sporadic cases.
5) `rtk-ag`: number of tests done using Antigen Rapid Test Kits (RTK-Ag)
6) `pcr`: number of tests done using Real-time Reverse Transcription Polymerase Chain Reaction (RT-PCR) technology

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
3) `beds`: number of available beds (with related medical infrastructure)
4) `admitted_x`: number of individuals in category `x` admitted, where `x` can be Person-Under-Investigation (PUI), COVID-19 positive, or non-COVID.
5) `discharged_x`: number of individuals in category `x` discharged
6) `pkrc_x`: total number of individuals in category `x` in PKRCs; this is a stock variable altered by flows from admissions and discharges


### Hospital

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: name of state, with similar qualification on exhaustiveness of date-state combos as PKRC data
3) `beds`
4) `beds_noncrit`
5) `admitted_pui`
6) `admitted_covid`
7) `admitted_total`
8) `discharged_pui`
9) `discharged_covid`
10) `discharged_total`
11) `hosp_covid`
12) `hosp_pui`
13) `hosp_noncovid`


### ICU

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: name of state, with similar qualification on exhaustiveness of date-state combos as PKRC data
3) `beds_icu`
4) `beds_icu_rep`
5) `beds_icu_total`
6) `beds_icu_covid`
7) `vent``vent_port`
8) `icu_covid`
9) `icu_pui`
10) `icu_noncovid`
11) `vent_covid`
12) `vent_pui`
13) `vent_sari`
14) `vent_noncovid`


### Deaths

1) `date`: yyyy-mm-dd format; data correct as of 1200hrs on that date
2) `state`: name of state (present in state file, but not country file)
3) `deaths_new`: deaths due to COVID-19 reported in the 24h since the last report
