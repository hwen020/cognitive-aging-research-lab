# Artificial fixture only. No HRS records or metadata.
set.seed(42)
args <- commandArgs(trailingOnly = TRUE)
work <- if (length(args)) args[1] else ".analysis-work"
dir.create(work, recursive = TRUE, showWarnings = FALSE)
n <- 60
id <- rep(seq_len(n), each = 4)
time <- rep(c(0, 2, 4, 6), n)
d <- data.frame(id = sprintf("S%03d", id), interview_year = 2000 + time,
                age_baseline = rep(sample(60:79, n, TRUE), each = 4),
                education_years = rep(sample(8:20, n, TRUE), each = 4),
                sex = rep(rep(1:2, length.out = n), each = 4),
                income = rnorm(length(id), 20, 4), hypertension = rbinom(length(id), 1, .4))
d$cognition <- 25 - .5 * time + rnorm(n)[id] + rnorm(n, 0, .2)[id] * time + rnorm(length(id), 0, .5)
d$cognition[seq(8, nrow(d), by = 13)] <- NA_real_
input <- file.path(work, "synthetic-hrs-framework-fixture.csv")
output <- file.path(work, "synthetic-hrs-framework-fixture.rds")
write.csv(d, input, row.names = FALSE)
exe <- file.path(R.home("bin"), "Rscript")
stopifnot(system2(exe, c("--vanilla", "analysis/r/hrs_framework.R", input, output)) == 0)
result <- readRDS(output)
stopifnot(result$participants == n, result$included_rows < nrow(d),
          is.finite(result$aic[["intercept"]]), is.finite(result$aic[["slope"]]))
cat("Synthetic longitudinal framework fixture passed.\n")
