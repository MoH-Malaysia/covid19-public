# Open data on COVID-19 in Malaysia

**The scope and granularity of data in this repo will evolve over time.**
+ Documentation and data descriptions contained within subfolders. 
+ Submit pull requests to [share your work for the community](/CONTRIB.md#share-your-work) or [request more data](/CONTRIB.md#data-requests).

---

### Cases and Testing

1) [`cases_malaysia.csv`](/epidemic/cases_malaysia.csv): Daily recorded COVID-19 cases at country level, as of 1200 of date.
2) [`cases_state.csv`](/epidemic/cases_state.csv): Daily recorded COVID-19 cases at state level, as of 1200 of date.
3) [`clusters.csv`](/epidemic/clusters.csv): Exhaustive list of announced clusters with relevant epidemiological datapoints, as of 2359 of date of update.
4) [`tests_malaysia.csv`](/epidemic/tests_malaysia.csv): Daily tests (note: not necessarily unique individuals) by type at country level, as of 1200 of date.

### Healthcare

1) [`pkrc.csv`](/epidemic/pkrc.csv): Flow of patients to/out of Covid-19 Quarantine and Treatment Centres (PKRC), with capacity and utilisation as of 2359 of date.
2) [`hospital.csv`](/epidemic/hospital.csv): Flow of patients to/out of hospitals, with capacity and utilisation as of 2359 of date.
3) [`icu.csv`](/epidemic/icu.csv): Capacity and utilisation of intensive care unit (ICU) beds as of 2359 of date.

### Deaths

1) [`deaths_malaysia.csv`](/epidemic/deaths_malaysia.csv): Daily deaths due to COVID-19 at country level, as of 1200 of date.
2) [`deaths_state.csv`](/epidemic/deaths_state.csv): Daily deaths due to COVID-19 at state level, as of 1200 of date.

### Vaccination

MoH collaborates with MoSTI and the COVID-19 Immunisation Task Force (CITF) to publish open data on Malaysia's vaccination rollout. All relevant data can be found at [this repo](https://github.com/CITF-Malaysia/citf-public).

### Mobility and Contact Tracing

1) [`checkin_malaysia.csv`](/mysejahtera/checkin_malaysia.csv): Daily checkins on MySejahtera at country level, as of 2359 of date.
2) [`checkin_state.csv`](/mysejahtera/checkin_state.csv): Daily checkins on MySejahtera at state level, as of 2359 of date.
3) [`checkin_malaysia_time.csv`](/mysejahtera/checkin_malaysia_time.csv): Time distribution of daily checkins on MySejahtera at country level, as of 2359 of date.
4) [`trace_malaysia.csv`](/mysejahtera/trace_malaysia.csv): Daily casual contacts traced and hotspots identified by HIDE, at country level, as of 2359 of date.

### Static data

1) [`population.csv`](/static/population.csv): Total, adult (≥18), and elderly (≥60) population at state level.

_Static data will (probably) remain unchanged for the duration of the program, barring an update from the source, e.g. if DOSM makes an update to population estimates. We provide this data here not to supersede the source, but rather to be transparent about the data we use to compute key statistics e.g. the % of the population that is vaccinated. We also hope this ensures synchronisation (across various independent analysts) of key statistics down to the Nth decimal place._
