# r_eda_script.R
library(DataExplorer)
library(rmarkdown)
args <- commandArgs(trailingOnly=TRUE)
input_file <- args[1]
output_file <- args[2]
df <- read.csv(input_file)
create_report(df, output_file = output_file, report_title = "Reporte EDA R")