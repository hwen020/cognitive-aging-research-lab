# Execute independently in an approved HRS environment without AI access.
# Input is a manually harmonized long-form CSV. Never pass microdata to an AI tool.
args <- commandArgs(trailingOnly = TRUE)
if (length(args) != 2L) stop("Usage: Rscript hrs_framework.R harmonized.csv private-aggregate-output.rds")
library(nlme)
d <- read.csv(args[1], colClasses = c(id = "character"))
fields <- c("id", "interview_year", "cognition", "age_baseline", "education_years", "sex", "income", "hypertension")
stopifnot(all(fields %in% names(d)), !anyNA(d[c("id", "interview_year")]),
          !anyDuplicated(d[c("id", "interview_year")]))
d <- d[order(d$id, d$interview_year), ]
d$time <- d$interview_year - ave(d$interview_year, d$id, FUN = min)
d$last_observed <- ave(ifelse(is.na(d$cognition), NA, d$time), d$id,
                      FUN = function(x) if (all(is.na(x))) NA_real_ else max(x, na.rm = TRUE))
keep <- complete.cases(d[, fields])
used <- d[keep, ]
stopifnot(length(unique(used$id)) >= 30L, any(duplicated(used$id)))
f <- cognition ~ time * education_years + age_baseline + sex + income + hypertension
intercept <- lme(f, random = ~1 | id, data = used, method = "ML")
slope <- tryCatch(lme(f, random = ~time | id, data = used, method = "ML"),
                  error = function(e) NULL)
fixed <- if (length(unique(used$id)) <= 2000L) {
  lm(cognition ~ factor(id) + time + time:education_years + income + hypertension, data = used)
} else NULL
result <- list(missing = colMeans(is.na(d[, fields])),
               observed_by_year = as.data.frame(table(d$interview_year, is.na(d$cognition))),
               follow_up = unname(quantile(unique(d[c("id", "last_observed")])$last_observed,
                                          c(0, .25, .5, .75, 1), na.rm = TRUE)),
               included_rows = nrow(used), participants = length(unique(used$id)),
               intercept_model = summary(intercept)$tTable,
               slope_model = if (is.null(slope)) NULL else summary(slope)$tTable,
               aic = c(intercept = AIC(intercept), slope = if (is.null(slope)) NA else AIC(slope)),
               residual_acf = ACF(intercept, maxLag = 3),
               fixed_effects_sensitivity = if (is.null(fixed)) NULL else
                 coef(summary(fixed))[intersect(c("income", "hypertension", "time", "time:education_years"),
                                                rownames(coef(summary(fixed)))), , drop = FALSE])
saveRDS(result, args[2])
