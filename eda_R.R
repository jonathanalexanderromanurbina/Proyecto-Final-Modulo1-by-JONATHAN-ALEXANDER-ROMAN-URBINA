args <- commandArgs(trailingOnly = TRUE)
input_file <- args[1]
output_file <- args[2]

# Cargar paquetes
suppressMessages(library(dplyr))

# Leer archivo CSV
df <- read.csv(input_file)

# Generar resumen
summary_data <- capture.output(summary(df))
writeLines(summary_data, output_file)
