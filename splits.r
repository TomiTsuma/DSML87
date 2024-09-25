# options(repos = "https://cran.r-project.org")

# install.packages('prospectr')
# install.packages('data.table')
# install.packages('ggplot2')
# install.packages('stringr')
# install.packages('terra')
# install.packages('sp')
# install.packages('units')
# install.packages('sf')
# install.packages('raster')
# install.packages('reshape2')
# install.packages('plyr')
# install.packages('clhs')

library(prospectr)
library(data.table)
library(ggplot2)
library(stringr)
library(terra)
library(clhs)

# chemicals <- c('boron', 'calcium', 'clay', 'copper', 'ec_salts',
#                'exchangeable_acidity', 'iron', 'magnesium', 'manganese', 'phosphorus',
#                'potassium', 'sand', 'silt', 'sodium', 'sulphur', 'zinc', 'ph')
# Read the CSV file
# Replace "your_file.csv" with the actual path to your CSV file
data <- read.csv("/home/tom/DSML125/inputFiles/modeling-instructions.csv", stringsAsFactors = FALSE)

# Extract the "chemicals" column and store it as an array
chemicals <- as.array(data$chemical)


args <- commandArgs(trailingOnly = TRUE)
chem <- args[1]

split <- function(path_to_spc, path_to_rds, path_to_splits){
  # for (chem in chemicals) {
    print(paste0("chemical : ", chem))
    #     print(chemical)
    df <- fread(paste0(path_to_spc , chem , "_spc.csv"), header=TRUE)
    # print(paste0("Dimensions for the dataset to split : ",dim(df)))
    
    if("sample_code" %in% colnames(df)){
      rownames(df) <- df$sample_code
      df$sample_code <- NULL
    }
    else if("sample_id" %in% colnames(df)){
      rownames(df) <- df$sample_id
      df$sample_id <- NULL
    }
    else{
      rownames(df) <- df$V1
      df$V1 <- NULL
    }
    sg <- savitzkyGolay(X = df, m = 1, p = 3, w = 21, delta.wav = 1); 
    pca <- prcomp(t(sg), scale=FALSE); 
    saveRDS(pca, file = paste0(path_to_rds, chem, "_pca.rds"))
    #     rownames(df) <- df$V1
    # PCA summary
    summary(pca)
    
    
    head(pca)
    
    rownames(pca) 
    
    
    
    # select the components with threshold (95%) explained variance 
    #PCA(0.95)<____________________________==============
    pca_sub <- pca$rotation[, 0:6]
    
    dim(pca_sub)
    
    # calculate 10% of total number of samples
    n_sel <- round(nrow(pca_sub) * 0.15)
    # print(n_sel)
    # convert to dataframe
    r.df <- data.frame(pca_sub)
    
    # assign sample codes
    rownames(r.df) <- rownames(df)
    head(r.df)
    # print(r.df)
    
    # perform conditioned Latin Hypercube Sampling
    res_test<-clhs(x=r.df, size=n_sel, iter=10000, simple = FALSE) 
    
    # res_test <- randomLHS(n = nrow(r.df), k = n_sel)
    res_test$index_samples
    test<-r.df[res_test$index_samples,]
    head(test)
    
    # plot only the objective function
    #plot(res_test, mode = "obj")
    
    # compare the distribution in the original object and in the sampled result
    #plot(res_test, mode = c("obj", "box"))
    
    # check dimensions
    # print(dim(test))
    
    
    rownames(res_test$sampled_data)
    
    # save 10% selection sample codes
    write.csv(rownames(res_test$sampled_data),paste0(path_to_splits, "/", chem, "_test_sample_codes.csv"))
    
    remainder <- r.df[!rownames(r.df) %in% rownames(res_test$sampled_data), ]
    
    dim(remainder)
    
    dim(r.df)
    
    n_sel_valid <- round(nrow(remainder) * 0.1)
    
    n_sel
    
    n_sel_valid
    
    # perform conditioned Latin Hypercube Sampling
    valid_res<-clhs(x=remainder, size=n_sel_valid, iter=10000, simple = FALSE) 
    valid_res$index_samples
    valid<-r.df[valid_res$index_samples,]
    # head(valid)
    
    
    
    
    # plot only the objective function
    #plot(valid_res, mode = "obj")
    
    # compare the distribution in the original object and in the sampled result
    #plot(valid_res, mode = c("obj", "box"))
    
    # check dimensions
    dim(valid)
    
    # save 10% selection sample codes
    write.csv(rownames(valid_res$sampled_data),paste0(path_to_splits, "/", chem, "_valid_sample_codes.csv"))
    
    
    
    
    
    
    
    
    
    train <- remainder[!rownames(remainder) %in% rownames(valid_res$sampled_data), ]
    
    print(dim(train))
    
    dim(r.df)
    
    dim(remainder)
    
    write.csv(rownames(train),paste0(path_to_splits, "/", chem, "_train_sample_codes.csv"))
    
    
    rownames(train)
    
    
  # }
}

split("/home/tom/DSML125/DSML87/outputFiles/",
          "/home/tom/DSML125/DSML87/outputFiles/rds/", "/home/tom/DSML125/DSML87/outputFiles/splits")
