# Documentation for linelists

### Cases

From the 4th of June onwards, the cases linelist is accessible as a single file via Amazon S3 in either [CSV](https://moh-malaysia-covid19.s3.ap-southeast-1.amazonaws.com/linelist_cases.csv) or [parquet](https://moh-malaysia-covid19.s3.ap-southeast-1.amazonaws.com/linelist_cases.parquet) format. Prior to the 4th of June, the cases linelist was split into chunks of 500,000 cases each to manage file size - we have ported it over to Amazon S3 to avoid this practice. The S3 URLs function in the same way as GitHub raw endpoints, and can be accessed directly from (for example) a Jupyter Notebook. 

All aggregated data on cases is derived from this linelist.

1) `date`: yyyy-mm-dd format; date of case
2) `days_doseN` number of days between the positive sample date and the individual's first/second/third dose (if any); values 0 or less are nulled
3) `brandN`: `p` = Pfizer, `s` = Sinovac, `a` = AstraZeneca, `c` = Cansino, `m` = Moderna, `h` = Sinopharm, `j` = Janssen, `u` = unverified (pending sync with VMS) 
4) `import`: binary variable with 1 denoting an imported case and 0 denoting local transmission
5) `cluster`: binary variable with 1 denoting cluster-based transmission and 0 denoting an unlinked case
6) `symptomatic`: binary variable with 1 denoting an individual presenting with symptoms at the point of testing 
7) `state`: state of residence, coded as an integer (refer to [`param_geo.csv`](https://github.com/MoH-Malaysia/covid19-public/blob/main/epidemic/linelist/param_geo.csv))
8) `district`: district of residence, coded as an integer (refer to [`param_geo.csv`](https://github.com/MoH-Malaysia/covid19-public/blob/main/epidemic/linelist/param_geo.csv))
9) `age`: age as an integer, with `-1` denoting missing data
10) `male`: binary variable with 1 denoting male and 0 denoting female
11) `malaysian`: binary variable with 1 denoting Malaysian and 0 denoting non-Malaysian
12) `comorb`: binary variable with 1 denoting that the individual has comorbidities and 0 denoting no comorbidities declared

### Deaths

All aggregated data on deaths is derived from this linelist, which can also be accessed via Amazon S3 in [parquet](https://moh-malaysia-covid19.s3.ap-southeast-1.amazonaws.com/linelist_deaths.parquet) format.

_Note: The deaths linelist was released prior to the cases linelist. As such, it is formatted differently, because several optimisations had to be made to reduce the size of the cases linelist (in particular, coding as many things as possible as integers). In order not to break anyone's scripts, we are not changing the original format of the deaths linelist._

1) `date`: yyyy-mm-dd format; date of death
2) `date_announced`: date on which the death was announced to the public (i.e. registered in the public linelist)
3) `date_positive`: date of positive sample
4) `date_doseN`: date of the individual's first/second/third dose (if any)
5) `brandN`:  `p` = Pfizer, `s` = Sinovac, `a` = AstraZeneca, `c` = Cansino, `m` = Moderna, `h` = Sinopharm, `j` = Janssen, `u` = unverified (pending sync with VMS) 
6) `state`: state of residence
7) `age`: age as an integer; note that it is possible for age to be 0, denoting infants less than 6 months old
8) `male`: binary variable with 1 denoting male and 0 denoting female
9) `bid`: binary variable with 1 denoting brought-in-dead and 0 denoting an inpatient death
10) `malaysian`: binary variable with 1 denoting Malaysian and 0 denoting non-Malaysian
11) `comorb`: binary variable with 1 denoting that the individual has comorbidities and 0 denoting no comorbidities declared
