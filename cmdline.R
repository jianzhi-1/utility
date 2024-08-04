args = commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  stop("Please provide two arguments: an integer and a string.")
}

num <- as.numeric(args[1])
text <- args[2]

if (is.na(num)) {
  stop("The first argument must be an integer.")
}

print(paste("The integer is:", num))
print(paste("The string is:", text))
