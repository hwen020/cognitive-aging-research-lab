source("analysis/r/fit.R")
markers <- c("crp", "ptau", "nfl")
fits <- lapply(markers, function(marker) {
  baseline <- cohort[cohort$visit_year == 0, c("participant_id", marker)]
  cohort$marker_baseline <- baseline[[marker]][match(cohort$participant_id, baseline$participant_id)]
  cohort$marker_within <- cohort[[marker]] - cohort$marker_baseline
  formula <- as.formula(paste(
    "cognitive_score ~ visit_year * deprivation +", adjustment, "+ marker_baseline + marker_within"
  ))
  fit_model(formula, cohort, marker)
})
coefficients <- do.call(rbind, lapply(fits, function(fit) fit$coefficients))
coefficients$q_bh <- NA_real_
marker_terms <- coefficients$term %in% c("marker_baseline", "marker_within")
coefficients$q_bh[marker_terms] <- p.adjust(coefficients$p[marker_terms], method = "BH")
write.csv(coefficients, file.path(out, "biological_coefficients.csv"), row.names = FALSE)
write.csv(do.call(rbind, lapply(fits, function(fit) fit$diagnostics)),
          file.path(out, "biological_diagnostics.csv"), row.names = FALSE)
