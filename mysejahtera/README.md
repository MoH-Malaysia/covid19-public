## Documentation for vaccination datasets

### File naming convention

1) `vax_malaysia.csv`: Static name; file is updated by 0200hrs daily
2) `vax_state.csv`: Static name; file is updated by 0200hrs daily

### Variables

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `state`: Name of state (present in state file, but not country file)
3) `dose1_daily`: 1st doses delivered between 0000 and 2359 on date
4) `dose2_daily`: 2nd doses delivered between 0000 and 2359 on date; note that this will not equal the number of people who were fully vaccinated on a given date when Malaysia begins using single-dose vaccines (e.g. CanSino).
5) `total_daily` = `dose1_daily` + `dose2_daily`
6) `dose1_cumul` = sum of `dose1_daily` for all T <= `date`
7) `dose2_cumul` = sum of `dose2_daily` for all T <= `date`
8) `total_cumul` = `dose1_cumul` + `dose2_cumul`

### Methodological choices
+ For the purposes of reporting doses delivered, `total_cumul` = `dose1_cumul` + `dose2_cumul`. However, when counting the number of _unique individuals_ who have been vaccinated, note that `dose2_cumul` is a perfect subset of `dose1_cumul` - everyone who received a 2nd dose also shows up in the 1st dose count. As such, the total number of individuals who have received _at least_ 1 dose is exactly equal to `dose1_cumul`. 
+ With substantial outreach efforts in areas with poor internet access, vaccinations (which are normally tracked in real time) have to be documented offline (think Excel sheets and paper forms). Given that outreach programs may last days at a time, records of these vaccinations may only be uploaded and consolidated a few days after the day on which they occured. Consequently, we may revise the dataset from time to time if more data is reported for dates already contained within the datasets. These revisions will typically cause vaccination counts to increase, though minor decreases may be observed if there are corrections to dosage dates after they are recorded and published under another day's data.
     + The first such revision was made on [17th July](https://github.com/CITF-Malaysia/citf-public/commit/2f3100bce891e34c660471ac4dc96dddb911e6eb#diff-61b43ea1f6043e3ce51f4264320ef8907ad059425fc3bcf7cc9f4c20fac3b025).
