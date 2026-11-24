# VCAP Methods

Source: [Salthouse (2024), VCAP, University of Virginia Dataverse, V1.0](https://doi.org/10.18130/V3/QRCQ08).

Join Demographics, Test Dates and DigSym1 on SubjID and Occasion. Collapse identical selected rows and exclude conflicting keys. Require occasion 1, a documented baseline date, baseline test and complete baseline covariates. Require a valid date and score on each included occasion. Time is actual elapsed days divided by 365.2425. Digit Symbol is the number of correct matches in 120 seconds (0–133). The analysis retains raw score units and models baseline age centered at 60, education centered at 16, recorded sex and age-by-time interaction. Compare participant random intercept and correlated intercept/slope by ML AIC. Coefficient intervals use nlme's t approximation.
