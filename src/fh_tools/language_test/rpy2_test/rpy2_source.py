from rpy2 import robjects
robjects.r.source("FHSGACH3Py.R")
p = robjects.r['FHSGACH3Py']("reseries.csv", "VolSimu.csv", 123)

