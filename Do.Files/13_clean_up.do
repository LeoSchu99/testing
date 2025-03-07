cap log close
log using ${log}\13_clean_up.log, replace

/*
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	
	SIAB Preparation
	
	Clean up the data set
	
	
	Author(s): Wolfgang Dauth, Johann Eppelsheimer

	Version: 1.0
	Created: 2020-03-23
	
	~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
		
*/



********************************************************************************
* Sort the data
********************************************************************************
sort persnr jahr		// if yearly panel
*sort persnr nspell		// if spell data

********************************************************************************
* Declare panel structure
********************************************************************************
xtset persnr jahr		// if yearly panel
*xtset persnr nspell	// if spell data

********************************************************************************
* Drop unnecessary variables
********************************************************************************
*drop ...

********************************************************************************
* Order of variables
********************************************************************************
*order persnr jahr ...


********************************************************************************
* Compress the data
********************************************************************************
unab compVars : _all
unab exclude : persnr betnr
local compVars : list varlist - exclude		// excluding identifier variables
compress $compVars




log close
