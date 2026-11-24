# Aggregate-only analysis of independent NHANES cross-sections.
library(survey)
library(jsonlite)
args <- commandArgs(trailingOnly = TRUE)
input <- if (length(args)) args[1] else ".analysis-work/nhanes/cohort.csv"
output <- if (length(args) >= 2) args[2] else ".analysis-work/nhanes/results.json"
data <- read.csv(input)
data <- subset(data, mec4 > 0 & RIDSTATR == 2)
stopifnot(!anyDuplicated(data$SEQN), all(is.finite(data$mec4)), all(data$mec4 == data$WTMEC2YR / 2))
data$education <- factor(data$education, levels = c(5, 4, 3, 2, 1))
data$sex <- factor(data$RIAGENDR)
data$race <- factor(data$RIDRETH3)
data$wave <- factor(data$cycle)
data$psu <- interaction(data$cycle, data$SDMVSTRA, data$SDMVPSU, drop = TRUE)
data$stratum <- interaction(data$cycle, data$SDMVSTRA, drop = TRUE)
stopifnot(all(tapply(data$psu, data$stratum, function(x) length(unique(x))) >= 2))
data$sbp10 <- data$sbp / 10
options(survey.lonely.psu = "adjust", survey.adjust.domain.lonely = TRUE)
design <- svydesign(ids = ~psu, strata = ~stratum, weights = ~mec4, data = data, nest = TRUE)
older <- subset(design, RIDAGEYR >= 60)
outcomes <- c("dsst", "immediate", "delayed", "fluency")
social <- c("education", "pir", "RIDAGEYR", "sex", "race", "wave")
bio <- c("hba1c", "sbp10")
vars <- older$variables
sample_for <- function(fields) complete.cases(vars[, fields, drop = FALSE])
analyze <- function(outcome, covariates, domain = rep(TRUE, nrow(vars))) {
  keep <- sample_for(c(outcome, covariates)) & domain
  d <- older[keep, ]
  model <- svyglm(reformulate(covariates, outcome), design = d)
  tab <- coef(summary(model))
  ci <- confint(model, df = model$df.residual)
  fitted_values <- fitted(model)
  bins <- cut(rank(fitted_values, ties.method = 'first'), breaks = 8)
  diagnostics <- aggregate(cbind(fitted_values, residual = residuals(model)) ~ bins,
                           FUN = mean)
  diagnostics$bins <- NULL
  list(n = sum(keep), df = model$df.residual, formula = paste(deparse(formula(model)), collapse = ""),
       residual_bins = diagnostics, weighted_residual_rmse = sqrt(weighted.mean(residuals(model)^2, weights(d))),
       coefficients = data.frame(term = rownames(tab), estimate = tab[, 1], se = tab[, 2],
                                 p = tab[, 4], lower = ci[, 1], upper = ci[, 2], row.names = NULL))
}
desc <- setNames(lapply(outcomes, function(name) {
  d <- older[!is.na(vars[[name]]), ]
  model <- svymean(reformulate(name), d)
  ci <- confint(model, df = degf(d))
  list(n = nrow(d$variables), estimate = unname(coef(model)[1]), lower = ci[1, 1], upper = ci[1, 2])
}), outcomes)
social_models <- setNames(lapply(outcomes, analyze, covariates = social), outcomes)
bio_models <- setNames(lapply(outcomes, analyze, covariates = c(social, bio)), outcomes)
for (family in c("social_models", "bio_models")) {
  fits <- get(family)
  rows <- lapply(fits, function(fit) {
    terms <- fit$coefficients$term
    which(if (family == "social_models") grepl("^education|^pir$", terms) else terms %in% bio)
  })
  adjusted <- p.adjust(unlist(Map(function(fit, i) fit$coefficients$p[i], fits, rows)), "BH")
  offset <- 0
  for (name in names(fits)) {
    i <- rows[[name]]
    fits[[name]]$coefficients$q_bh <- NA_real_
    fits[[name]]$coefficients$q_bh[i] <- adjusted[offset + seq_along(i)]
    offset <- offset + length(i)
  }
  assign(family, fits)
}
common <- vars[sample_for(c("dsst", social, bio)), ]
prediction <- function(d) {
  train <- subset(d, cycle == 2011)
  test <- subset(d, cycle == 2013)
  stopifnot(!any(test$SEQN %in% train$SEQN))
  rhs <- setdiff(social, "wave")
  baseline <- lm(reformulate(rhs, "dsst"), data = train)
  extended <- lm(reformulate(c(rhs, bio), "dsst"), data = train)
  forest <- rpart::rpart(reformulate(c(rhs, bio), "dsst"), data = train,
                        control = rpart::rpart.control(cp = .02, xval = 0))
  y <- test$dsst
  predictions <- list(training_mean = rep(mean(train$dsst), nrow(test)),
                      social_linear = predict(baseline, test), augmented_linear = predict(extended, test),
                      augmented_tree = predict(forest, test))
  error <- function(pred) c(mae = mean(abs(y - pred)), rmse = sqrt(mean((y - pred)^2)),
                            r2 = 1 - sum((y - pred)^2) / sum((y - mean(y))^2))
  # Resample masked PSUs within strata, with models held fixed.
  set.seed(20261124)
  psus <- split(as.character(test$psu), test$stratum, drop = TRUE)
  indices <- replicate(500, unlist(lapply(psus, function(values) {
    keys <- unique(values)
    picked <- sample(keys, length(keys), replace = TRUE)
    unlist(lapply(picked, function(k) which(as.character(test$psu) == k)))
  })), simplify = FALSE)
  delta <- abs(y - predictions$augmented_linear) - abs(y - predictions$social_linear)
  list(train = nrow(train), test = nrow(test), overlap = 0L,
       metrics = lapply(predictions, function(p) as.list(error(p))),
       paired_mae_difference = mean(delta),
       paired_ci95 = unname(quantile(vapply(indices, function(i) mean(delta[i]), numeric(1)), c(.025, .975))))
}
analyze_curve <- function() {
  d <- older[sample_for(c("dsst", social, bio)), ]
  fit <- svyglm(dsst ~ education + pir + RIDAGEYR + sex + race + wave + hba1c +
                  sbp10 + I(sbp10^2) + I(hba1c^2), design = d)
  as.numeric(survey::regTermTest(fit, ~I(sbp10^2) + I(hba1c^2))$p)
}
result <- list(
  source = "CDC NHANES repeated cross-sectional 2011-2014",
  runtime = list(r = as.character(getRversion()), survey = as.character(packageVersion("survey"))),
  counts = list(total_demographics = nrow(read.csv(input)), mec = nrow(data), age_60_plus = nrow(vars),
                dsst_observed = sum(!is.na(vars$dsst)), social_primary = social_models$dsst$n,
                biological_primary = bio_models$dsst$n),
  missing_fraction = as.list(colMeans(is.na(vars[, c(outcomes, "education", "pir", "hba1c", "sbp10")]))),
  design = list(strata = length(unique(data$stratum)), psus = length(unique(data$psu)), domain_df = degf(older)),
  descriptive = desc, social = social_models, biological = bio_models,
  sensitivity = list(
    social_on_bio_complete = analyze("dsst", social, sample_for(bio)),
    social_age_70_plus = analyze("dsst", social, vars$RIDAGEYR >= 70),
    unadjusted_hba1c = analyze("dsst", "hba1c"),
    unadjusted_sbp = analyze("dsst", "sbp10"),
    bio_two_bp_readings = analyze("dsst", c(social, bio), vars$sbp_n >= 2),
    bio_quadratic_joint_p = analyze_curve(),
    predictor_correlation = unname(cor(common[, bio])[1, 2])
  ),
  prediction = prediction(common))
write_json(result, output, pretty = TRUE, auto_unbox = TRUE, digits = 12, na = "null")
cat("Wrote aggregate results:", output, "\n")
