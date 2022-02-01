# Documentation for Vaccination datasets

At present, primary vaccination (and vaccine registration) datasets are handled by the COVID-19 Immunisation Task Force (CITF) and can be found at the [CITF GitHub](https://github.com/CITF-Malaysia/citf-public). These datasets will be ported to the MoH GiHhub from 1st November. Supplementary datasets (published in September or later) were originally published on the MoH GitHub, and are documented below.


## Variables and Methodology

### Vaccination

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
2) `daily_partial`: number of individuals who received the first dose of a two-dose protocol
3) `daily_partial_adol`: subset (already included) of `daily_partial`, but for individuals aged 12-17 only
4) `daily_partial_child`: subset (already included) of `daily_partial`, but for individuals aged 5-11 only
5) `daily_full`: number of individuals who completed their original protocol (whether the 2nd dose of a two-dose protocol, or a single-dose protocol)
6) `daily_full_adol`: subset (already included) of `daily_full`, but for individuals aged 12-17 only
7) `daily_full_child`: subset (already included) of `daily_full`, but for individuals aged 5-11 only
8) `daily_booster`: number of individuals who received one dose beyond the original protocol
9) `daily`: total doses administered
10) `cumul_x`: cumulative doses falling into category `x`, where `x` is one of the daily categories
11) `brandX`: denotes the number of 1st, 2nd, or 3rd doses administered for that brand; note that `cansino2` is omitted as it is a single-dose protocol
12) `pendingX`: number of records with an indeterminate brand, usually due to errors synchronising with the Vaccine Management System (VMS) blockchain

### AEFIs

An adverse event following immunisation (AEFI) is any untoward medical occurrence which follows immunisation. AEFIs are not necessarily caused by the vaccine - they can be related to the vaccine itself, to the vaccination process (stress related reactions) or can occur independently from vaccination (coincidental). The datasets include cases reported through both the NPRA Reporting System and MySejahtera.


_Disclaimers:_ 
- _The data are unverified (i.e. self-declared) reports of adverse events, both minor and serious, that occur after immunisation._
- _The number of reports alone cannot used to reach conclusions about the existence, severity, frequency, or rates of AEFIs associated with vaccines._
- _Reported events are not always proven to have a causal relationship with the vaccine. Establishing causality requires additional investigation. Serious AEFI reports are always followed-up and investigated thoroughly for better understanding of the circumstances. However, our public data does not generally change based on information obtained from the investigation process (i.e. we do not reduce AEFI counts after the fact)._
- _The NPRA and MOH always consider the complexities mentioned above, in addition to various other factors, when analysing and monitoring vaccine safety._

1) `date`: yyyy-mm-dd format; data correct as of 2359hrs on that date
