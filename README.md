# Open data on COVID-19 in Malaysia

**We will continually maintain and improve the scope and granularity of data in this repo.**
+ Documentation and data descriptions contained within subfolders. 

---

**Epidemic**

1) [`cases_malaysia.csv`](/epidemic/cases_malaysia.csv): Daily recorded COVID-19 cases at country level, as of 1200 of date.
2) [`cases_state.csv`](/epidemic/cases_state.csv): Daily recorded COVID-19 cases at state level, as of 1200 of date.
3) [`deaths_malaysia.csv`](/epidemic/deaths_malaysia.csv): Daily deaths due to COVID-19 at country level, as of 1200 of date.
2) [`deaths_state.csv`](/epidemic/deaths_state.csv): Daily deaths due to COVID-19 at state level, as of 1200 of date.

**Vaccination**

MoH works together with MoSTI and the COVID-19 Immunisation Task Force (CITF) to publish open data on Malaysia's vaccination rollout. All relevant data can be found at [this repo](https://github.com/CITF-Malaysia/citf-public).

**MySejahtera**

1) [`checkin_malaysia.csv`](/epidemic/checkin_malaysia.csv): Daily checkins on MySejahtera at country level, as of 2359 of date.
2) [`checkin_malaysia_time.csv`](/epidemic/checkin_malaysia_time.csv): Time distribution of daily checkins on MySejahtera at country level, as of 2359 of date.
3) [`checkin_state.csv`](/epidemic/checkin_malaysia_time.csv): Daily checkins on MySejahtera at state level, as of 2359 of date.
4) [`trace_malaysia.csv`](/epidemic/trace_malaysia.csv): Daily casual contacts traced and hotspots identified by HIDE, at country level, as of 2359 of date.

**Static data**

1) [`population.csv`](/static/population.csv): Total, adult (18+), and elderly (60+) population at state level.

_Static data will (probably) remain unchanged for the duration of the program, barring an update from the source, e.g. if DOSM makes an update to population estimates. We provide this data here not to supersede the source, but rather to be transparent about the data we use to compute key statistics e.g. the % of the population that is vaccinated. We also hope this ensures synchronisation (across various independent analysts) of key statistics down to the Nth decimal place._
