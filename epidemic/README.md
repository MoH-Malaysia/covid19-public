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

1) `cluster`
2) `state` and `district`
3) `date_announced`
4) `date_last_onset`
5) `category`
6) `status`
7) `cases_new`
8) `cases_total`
9) `cases_active`
10) `tests`
11) `icu`
12) `deaths`
13) `recovered`


### Healthcare: PKRC

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date

### Healthcare: Hospital

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date

### Healthcare: ICU

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date

### Deaths

1) `date`: yyyy-mm-dd format; data correct as of 1200hrs on that date
2) `state`: name of state (present in state file, but not country file)
3) `deaths_new`: deaths due to COVID-19 reported in the 24h since the last report
