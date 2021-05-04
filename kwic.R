library(reticulate)
library(quanteda)

source_python("pickle_reader.py")
pickle_data <- read_pickle_file("data/pickle/hansard_p10")

dfm_2001 <- dfm(pickle_data[[17]][2])
df <- as.data.frame(kwic(pickle_data[[17]][2], pattern="wanita"))
df 
