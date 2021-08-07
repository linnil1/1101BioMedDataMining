# modified from step7 ValidateByIsolatedDataClassifier
import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import sklearn.metrics as skMetric
from sklearn.externals import joblib

from genepi.step7_validateByIsolatedData import IsolatedDataFeatureGenerator
from genepi.step5_crossGeneEpistasis_Logistic import PlotPolygenicScore

# test_name = "data/example_wgs.plink.filter.test"
# geneepi_folder = "./data/geneepi1"
# test_name = sys.argv[1]
# genotype = f'{test_name}.gen'
# phenotype = f'{test_name}.sample.onlypheno.csv'
genotype = sys.argv[1]
phenotype = sys.argv[2]
geneepi_folder = sys.argv[3]

model = f'{geneepi_folder}/crossGeneResult/Classifier.pkl'
feature = f'{geneepi_folder}/crossGeneResult/Feature.csv'

# load data
estimator = joblib.load(model)
np_genotype, np_phenotype = \
        IsolatedDataFeatureGenerator(feature, genotype, phenotype)

# predict
dict_y = {"target": list(np_phenotype[:, -1].astype(float)),
          "predict": estimator.predict(np_genotype),
          "predict_proba": estimator.predict_proba(np_genotype)}

# calculate statistic
tn, fp, fn, tp = skMetric.confusion_matrix(
        dict_y["target"], dict_y["predict"]).ravel()
fpr, tpr, _ = skMetric.roc_curve(
        dict_y["target"], np.array(dict_y["predict_proba"])[:, 1])
print(f"{tp=:3d} {fn=:3d}")
print(f"{fp=:3d} {tn=:3d}")

float_specificity = (tn     ) / (     fp      + tn)
float_sensitivity = (     tp) / (tp      + fn     )
float_accuracy =    (tn + tp) / (tp + fp + fn + tn)
float_precision =   (     tp) / (tp      + fn     )
float_recall =      (     tp) / (tp      + fn     )
float_f1 = float_precision * 2 * float_recall / \
           (float_precision + float_recall)
float_auc = skMetric.auc(fpr, tpr)
print(f"specificity: {float_specificity:.02f}")
print(f"sensitivity: {float_sensitivity:.02f}")
print(f"accuracy:    {float_accuracy:.02f}")
print(f"precision:   {float_precision:.02f}")
print(f"recall:      {float_recall:.02f}")
print(f"f1 score:    {float_f1:.02f}")
print(f"AUC:         {float_auc:.02f}")

# Plot
# * GenEpi_PGS_ISO.png
# * GenEpi_Prevalence_ISO.png
# * GenEpi_ROC_ISO.png
os.makedirs(geneepi_folder + "/isolatedValidation", exist_ok=True)
PlotPolygenicScore(dict_y["target"],
                   dict_y["predict"],
                   dict_y["predict_proba"],
                   geneepi_folder + "/isolatedValidation",
                   "ISO")
