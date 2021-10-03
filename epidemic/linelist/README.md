# Documentation for linelists

### Cases

The cases linelists are split into chunks of 500,000 cases each. Variable naming and order is consistent across all files (i.e. the source is a single database file; the data is chunked only when pushed to Github). This is to manage file size, especially if and when the dataset is deepened in future.

All aggregated data on cases available via the Github is derived from this linelist.

1) `date`: yyyy-mm-dd format; date of case
2) `days_dose1` number of days between the positive sample date and the individual's first dose (if any); values 0 or less are nulled
3) `days_dose2` number of days between the positive sample date and the individual's second dose (if any); values 0 or less are nulled
4) `vaxtype`: `p` = Pfizer, `s` = Sinovac, `a` = AstraZeneca, `c` = Cansino, `m` = Moderna, `h` = Sinopharm, `j` = Janssen, `u` = unverified (pending sync with VMS) 
5) `import`: binary variable with 1 denoting an imported case and 0 denoting local transmission
6) `cluster`: binary variable with 1 denoting cluster-based transmission and 0 denoting and unlinked case
7) `symptomatic`: binary variable with 1 denoting an individual presenting with symptoms at the point of testing 
8) `state`: state of residence, coded as an integer (refer to [`param_geo.csv`](https://github.com/MoH-Malaysia/covid19-public/blob/main/epidemic/linelist/param_geo.csv))
9) `district`: district of residence, coded as an integer (refer to [`param_geo.csv`](https://github.com/MoH-Malaysia/covid19-public/blob/main/epidemic/linelist/param_geo.csv))
10) `age`: age as an integer
11) `male`: binary variable with 1 denoting male and 0 denoting female
12) `malaysian`: binary variable with 1 denoting Malaysian and 0 denoting non-Malaysian

### Deaths

All aggregated data on deaths available via the Github is derived from this linelist. 

_Note: The deaths linelist was released prior to the cases linelist. As such, it is formatted differently, because several optimisations had to be made to reduce the size of the cases linelist (in particular, coding as many things as possible as integers). In order not to break anyone's scripts, we are not changing the original format of the deaths linelist._

1) `date`: yyyy-mm-dd format; date of death
2) `date_announced`: date on which the death was announced to the public (i.e. registered in the public linelist)
3) `date_positive`: date of positive sample
4) `date_dose1`: date of the individual's first dose (if any)
5) `date_dose2`: date of the individual's second dose (if any)
6) `vaxtype`:  `p` = Pfizer, `s` = Sinovac, `a` = AstraZeneca, `c` = Cansino, `m` = Moderna, `h` = Sinopharm, `j` = Janssen, `u` = unverified (pending sync with VMS) 
7) `state`: state of residence
8) `age`: age as an integer; note that it is possible for age to be 0, denoting infants less than 6 months old
9) `male`: binary variable with 1 denoting male and 0 denoting female
10) `bid`: binary variable with 1 denoting brought-in-dead and 0 denoting an inpatient death
11) `malaysian`: binary variable with 1 denoting Malaysian and 0 denoting non-Malaysian
12) `comorb`: binary variable with 1 denoting that the individual has comorbidities and 0 denoting no comorbidities declared
