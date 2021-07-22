# Documentation for MySejahtera datasets

_Note: As per the MySejahtera privacy policy, individual-level check-in data is purged after 90 days. These summary statistics are stored only as aggregated totals; MySejahtera does not store the underlying data. Consequently, data revisions are not possible for dates more than 90 days ago, even if an inconsistency is spotted._

## File naming convention

1) `checkin_malaysia.csv`: Static name; file is updated by 1500hrs daily
2) `checkin_malaysia_time.csv`: Static name; file is updated by 1500hrs daily
3) `trace_malaysia.csv`: Static name; file is updated by 1500hrs daily

## Variables and Methodology

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `checkins`: number of checkins at all locations registered on MySejahtera
3) `unique_ind`: number of unique accounts which checked in
4) `unique_loc`: number of unique premises checked into
5) `i`: in the time density file, checkins are aggregated by half-hour buckets, giving 48 in total; bucket `i` corresponds to the ith half-hour slot of the day. for instance, `i = 0` corresponds to 0000 - 0029; `i = 31` corresponds to 1500 - 1529.
6) `casual_contacts`: number of casual contacts identified and notified by CPRC's automated contact tracing system
7) `hide_large`: number of large hotspots identified by CPRC's hotspot identification system
8) `hide_small`: number of small hotspots identified by CPRC's hotspot identification system
