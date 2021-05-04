library(reticulate)
library(quanteda)

source_python("pickle_reader.py")
pickle_data <- read_pickle_file("data/adj/adjs_fil")

dfm_wc <- dfm(pickle_data)
textplot_wordcloud(dfm_wc, min_count=0, 
                   max_words=1000,
                   rotation=0,
                   min_size=0.1,
                   random_color=T)   
