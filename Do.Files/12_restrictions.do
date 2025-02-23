cap log close
log using ${log}\12_restrictions.log, replace



/*
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	SIAB Preparation
	
	Restricts the data to certain groups
	
	On default most commands are commented out. Users should uncomment and adjust selected lines.
	
	
	Author(s): Wolfgang Dauth, Johann Eppelsheimer

	Version: 1.0
	Created: 2020-03-23
	
	
	Comments: 
	Users can also run this do-file on the finished clean_siab.dta.
	
	Note, that this do-file can be very handy if you have several related research projects. 
	For instance, you could generate one base version of siab_clean.dta	and then create several
	'offsprings' by running 12_restrictions.do with different settings.
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
*/



********************************************************************************
* Data source
********************************************************************************
tab quelle

* keep if quelle == 1		// BeH  (Employee History)
* keep if quelle == 2		// LEH  (Benefit Recipient History)
* keep if quelle == 3		// LHG  (Unemployment Benefit II Recipient History)
* keep if quelle == 4		// MTH  (Participants in Measure History)
* keep if quelle == 5		// XMTH (Participants in Measure History)
* keep if quelle == 6		// ASU  (Jobseeker History)
* keep if quelle == 7		// XASU (Jobseeker History)


********************************************************************************
* Years
********************************************************************************
tab jahr

* keep if jahr >= 1975
* keep if jahr <= 2017



********************************************************************************
* Age limits
********************************************************************************
sum age

* drop if age < 18
* drop if age > 64


********************************************************************************
* Male/female
********************************************************************************
tab frau, m

* drop if frau == 0			// keep women only
* drop if frau == 1			// keep men only
* drop if missing(frau)		// drop missings



********************************************************************************
* Occupational status
********************************************************************************
tab erwstat, m

* keep if erwstat == 101							// only keep employees liable to social security ("Sozialversicherungspflichtig Beschaeftigte")

* drop if erwstat < 100								// drop if not in employment

* drop if missing(erwstat)							// drop if missing employment status

* drop if inlist(erwstat, 102, 121, 122, 141)		// drop trainees
* drop if inlist(erwstat, 109, 209)					// drop marginal part-time workers
* drop if inlist(erwstat, 105, 106)					// drop interns/trainees
* drop if inlist(erwstat, 140, 141, 142, 143)		// drop sailors
* drop if inlist(erwstat, 123)						// drop voluntary social/ecological year, ...
* drop if inlist(erwstat, 103, 119)					// drop partial retirement
* drop if inlist(erwstat, 112)						// drop family member workers in agriculture
* drop if inlist(erwstat, 203)						// drop artists
* drop if inlist(erwstat, 118, 205)					// drop casual workers
* drop if inlist(erwstat, 201)						// drop employees registered within households
* drop if inlist(erwstat, 104, 120, 124, 142)		// drop other groups with less than 100 workers
* drop if inlist(erwstat, 599)						// drop others



********************************************************************************
* Occupations
********************************************************************************
tab beruf, m
tab beruf2010_3, m

* drop ...


********************************************************************************
* Full-time
********************************************************************************
tab teilzeit, m

* keep if teilzeit == 0		// keep only full-time workers



********************************************************************************
* Wages below marginal part-time income threshold ("Geringfuegigkeitsgrenze")
********************************************************************************
sum tentgelt
tab marginal

* drop if marginal == 1 & quelle == 1	// drop workers below marginal part-time income threshold



********************************************************************************
* Missing establishment identifier
********************************************************************************
count if missing(betnr) & quelle == 1

* drop if missing(betnr) & quelle == 1

/*
	Comment:
	
	The variables betnr refers to the workplace of individuals.
	Hence, people not in employment have missings in this variable!
*/


********************************************************************************
* Missing regional information of WORKPLACE
********************************************************************************
count if missing(ao_bula) & quelle == 1

* drop if missing(ao_bula) & quelle == 1

/*
	Comment:
	
	The variables ao_bula refers to the workplace of individuals.
	Hence, people not in employment have missings in this variable!
*/


********************************************************************************
* WORKPLACE in East/West
********************************************************************************
tab ao_bula east, m

* keep if east == 0									// workplace in West (excl. Berlin) (drops all non-working individuals!)
* keep if east == 1 								// workplace in East (incl. Berlin) (drops all non-working individuals!)
* keep if ao_bula <= 11								// workplace in West (incl. Berlin) (drops all non-working individuals!)
* keep if inlist(ao_bula, 11, 12, 13, 14, 15, 16)	// workplace in East (incl. Berlin) (drops all non-working individuals!)

/* 
	Comment:
	
	east = 1: workplace in East Germany
	east = 0: workplace in West Germany
	Berlin is assigned to East
	
	For further details see ao_bula (from BHP).
	
	The variables east and ao_bula refer to the workplace of individuals.
	Hence, people not in employment have missings in these variables!
*/


********************************************************************************
* Other restrictions
********************************************************************************
* ...




log close
