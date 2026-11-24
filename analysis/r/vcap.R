library(nlme)
library(jsonlite)
args <- commandArgs(trailingOnly = TRUE)
d <- read.csv(args[1])
d$age_c <- d$age0 - 60
d$educ_c <- d$educ0 - 16
d$sex <- factor(d$sex0)
f <- score ~ years * age_c + educ_c + sex
d$returned <- ave(d$years, d$id, FUN=length) >= 2
fit <- function(data, random, formula=f) lme(formula, data=data, random=random, method="ML", na.action=na.fail)
ri <- fit(d, ~1|id)
rs <- tryCatch(fit(d, ~years|id), error=function(e) NULL)
primary <- if (is.null(rs)) ri else rs
pack <- function(m) {
 t <- summary(m)$tTable
 q <- qt(.975, t[, "DF"])
 data.frame(term=rownames(t), estimate=t[, "Value"], lower=t[, "Value"]-q*t[, "Std.Error"],
            upper=t[, "Value"]+q*t[, "Std.Error"], row.names=NULL)
}
# First observed repeat can introduce a level shift. Estimate jointly with elapsed time.
d$retest <- as.integer(d$occasion > 1)
practice <- fit(d, ~1|id, update(f, . ~ . + retest))
returning <- fit(subset(d, returned), ~1|id)
bins <- cut(d$years, c(-.001, .001, 2, 4, 6, 8, Inf), include.lowest=TRUE)
trajectory <- lapply(split(seq_len(nrow(d)), bins), function(i) {
 if (length(unique(d$id[i])) < 30) return(NULL)
 list(n=length(i), participants=length(unique(d$id[i])), mean_time=mean(d$years[i]), mean_score=mean(d$score[i]))
})
v <- residuals(primary, type="normalized")
result <- list(n=nrow(d), participants=length(unique(d$id)),
               primary=if (is.null(rs)) "random intercept" else "random intercept and slope",
               intercept_aic=AIC(ri), slope_aic=if (is.null(rs)) NULL else AIC(rs),
               slope_converged=!is.null(rs),
               slope_sd=if (is.null(rs)) NULL else as.numeric(VarCorr(rs)[2, "StdDev"]),
               coefficients=pack(primary), practice=pack(practice), returning=pack(returning),
               residual_quantiles=unname(quantile(v, c(.025,.5,.975))),
               residual_lag1=ACF(primary,maxLag=1,resType="normalized")$ACF[2],
               trajectory=Filter(Negate(is.null), trajectory),
               runtime=list(R=as.character(getRversion()),nlme=as.character(packageVersion("nlme"))))
write_json(result,args[2],auto_unbox=TRUE,pretty=TRUE,digits=10,na="null")
