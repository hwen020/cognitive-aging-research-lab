library(nlme)
# Balanced visits make the random-intercept slope equal the centered within-person slope.
person <- rep(seq_len(12), each = 4)
year <- rep(0:3, times = 12)
score <- 100 + person - 2 * year + rep(c(1, -1, -1, 1), 12) * (person / 30)
fit <- lme(score ~ year, random = ~1 | person, data = data.frame(person, year, score))
stopifnot(abs(fixef(fit)[["year"]] - (-2)) < 1e-8)
cat("Verified random-intercept slope against analytic -2\n")
