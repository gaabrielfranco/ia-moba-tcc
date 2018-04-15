#!/bin/bash
# Variance experiments
./ga_feature_selection.py ga_temporary_output/ga_test_variance_noout.csv --lang pt --metric v --mins 3 --maxs 9 --verbose --pltfile ga_temporary_output/variance_noout.png
./ga_feature_selection.py ga_temporary_output/ga_test_variance_outliers.csv --lang pt --metric v --mins 3 --maxs 9 --verbose --pltfile ga_temporary_output/variance_outliers.png --wo
# Inertia experiments
#./ga_feature_selection.py ga_temporary_output/ga_test_inertia_noout.csv --lang pt --metric i --mins 3 --maxs 9 --verbose
#./ga_feature_selection.py ga_temporary_output/ga_test_inertia_outliers.csv --lang pt --metric i --mins 3 --maxs 9 --verbose --wo
# Silhouette with euclidean
./ga_feature_selection.py ga_temporary_output/ga_test_silhouette_e_noout.csv --lang pt --metric se --mins 3 --maxs 9 --verbose
./ga_feature_selection.py ga_temporary_output/ga_test_silhouette_e_outliers.csv --lang pt --metric se --mins 3 --maxs 9 --verbose --wo
# Silhouette with cosine
./ga_feature_selection.py ga_temporary_output/ga_test_silhouette_c_noout.csv --lang pt --metric sc --mins 3 --maxs 9 --verbose
./ga_feature_selection.py ga_temporary_output/ga_test_silhouette_c_outliers.csv --lang pt --metric sc --mins 3 --maxs 9 --verbose --wo

