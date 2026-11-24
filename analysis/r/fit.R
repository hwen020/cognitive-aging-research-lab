args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("Usage: Rscript analysis/r/fit.R input.csv output-directory")
library(nlme)
cohort <- read.csv(args[1], stringsAsFactors = TRUE)
out <- args[2]
dir.create(out, recursive = TRUE, showWarnings = FALSE)

cohort$deprivation <- relevel(cohort$deprivation, ref = "Low")
cohort$age_centered <- cohort$age_at_baseline - 69
cohort$education_centered <- cohort$education_years - 14
adjustment <- "visit_year * (age_centered + sex + education_centered + hypertension)"
social_formula <- as.formula(paste("cognitive_score ~ visit_year * deprivation +", adjustment))

fit_model <- function(formula, data, label) {
  used <- data[complete.cases(model.frame(formula, data, na.action = na.pass)), ]
  model <- lme(formula, random = ~1 | participant_id, data = used, method = "REML", na.action = na.fail)
  summary_table <- summary(model)$tTable
  ci <- qt(.975, df = summary_table[, "DF"]) * summary_table[, "Std.Error"]
  coefficients <- data.frame(
    model = label, term = rownames(summary_table), estimate = summary_table[, "Value"],
    se = summary_table[, "Std.Error"], df = summary_table[, "DF"],
    ci_lower = summary_table[, "Value"] - ci, ci_upper = summary_table[, "Value"] + ci,
    p = summary_table[, "p-value"], row.names = NULL
  )
  residual <- residuals(model, type = "normalized")
  correlation <- ACF(model, maxLag = 1, resType = "normalized")
  random_sd <- as.numeric(VarCorr(model)[1, "StdDev"])
  diagnostics <- data.frame(
    model = label, formula = paste(deparse(formula), collapse = " "),
    n = nrow(used), participants = length(unique(used$participant_id)),
    excluded_rows = nrow(data) - nrow(used),
    random_intercept_sd = random_sd, residual_sd = model$sigma,
    residual_fit_correlation = cor(residual, fitted(model)),
    residual_q025 = quantile(residual, .025), residual_q975 = quantile(residual, .975),
    residual_lag1_acf = correlation$ACF[correlation$lag == 1],
    r_version = as.character(getRversion()), nlme_version = as.character(packageVersion("nlme"))
  )
  list(coefficients = coefficients, diagnostics = diagnostics)
}

social <- fit_model(social_formula, cohort, "social")
write.csv(social$coefficients, file.path(out, "social_coefficients.csv"), row.names = FALSE)
write.csv(social$diagnostics, file.path(out, "social_diagnostics.csv"), row.names = FALSE)
