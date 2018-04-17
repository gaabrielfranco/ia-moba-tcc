#!/bin/bash
# Variance experiments
./ga_feature_selection.py --lang pt --metric v --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_variance.csv
./ga_feature_selection.py --lang pt --metric v --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_variance_outliers.csv --wo
# Inertia experiments
./ga_feature_selection.py --lang pt --metric i --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_inertia.csv
./ga_feature_selection.py --lang pt --metric i --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_inertia_outliers.csv --wo
# Silhouette with euclidean
./ga_feature_selection.py --lang pt --metric se --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_silhouette_e.csv
./ga_feature_selection.py --lang pt --metric se --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_silhouette_e_outliers.csv --wo
# Silhouette with cosine
./ga_feature_selection.py --lang pt --metric sc --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_silhouette_c.csv
./ga_feature_selection.py --lang pt --metric sc --selec bin --ngen 300 --max_no_improv 0.2 --pop 50 --mincxpb 0.8 --elsize 0.1 --maxs 9 --divfac 0.5 --verbose files/output_ga/ga_definitive_silhouette_c_outliers.csv --wo

