# CEST-LA-vie
CSV Error Analysis Significant figure TabuLAtor (vie to finish the pun)

Usage:

python ErrorPlusSigFig.py \[ExperimentData.csv]

ExperimentData.csv should be formatted with the first line being column headers, with either 
  1) No tag : These columns will be copied as is into the output tables
  2) "\[ColumnName]\_T\[N]" Where ColumnName is the name of the column, with no spaces, and N is a natural number: 
     These columns represent trial data, and columns with the same ColumnName will be combined into a ColumnName_BST and ColumnName_ERR in the error analysis output, and into a single column ColumnName in the SigFig output.
  3) CALC_\[ColumnName]: These columns will be populated with calculated values, based on the expression in the second row. They will generate an "ColumnName\_BST" and "ColumnName\_ERR" in the error analysis output, and a combined "ColumnName" in the SigFig output. 

(NOTE: CALC_\[ColumnTitle] columns can only do calculations based on columns to their left, and must be space delimited:

  Imagine Dataset "R_T1,R_T2,R_T3,I_T1,I_T2,I_T3,CALC_V"
  
  In the second line of CALC_V,
  
    WORKS: I * R
    
    FAILS: I\*R
)
