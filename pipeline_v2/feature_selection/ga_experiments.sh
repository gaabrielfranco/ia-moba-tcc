#!/bin/bash

#Using all database
# Silhouette with cosine
./exact_solution_setpack.py --lang pt --metric cosine --db all --save_log output_ga/all/exact_setpack_cosine.csv
./ga_fs_setpack.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/all/ga_setpack_cosine.csv
# Silhouette with euclidean
./exact_solution_setpack.py --lang pt --metric euclidean --db all --save_log output_ga/all/exact_setpack_euclidean.csv
./ga_fs_setpack.py --lang pt --metric se --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/all/ga_setpack_euclidean.csv
# Variance experiments
./exact_solution_setpack.py --lang pt --metric variance --db all --save_log output_ga/all/exact_setpack_variance.csv
./ga_fs_setpack.py --lang pt --metric v --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/all/ga_setpack_variance.csv
# Inertia experiments
./exact_solution_setpack.py --lang pt --metric inertia --db all --save_log output_ga/all/exact_setpack_inertia.csv
./ga_fs_setpack.py --lang pt --metric i --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/all/ga_setpack_inertia.csv

#Using std database
# Silhouette with cosine
./exact_solution_setpack.py --lang pt --metric cosine --save_log output_ga/std/exact_setpack_cosine.csv
./ga_fs_setpack.py --lang pt --metric sc --selec bin --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/std/ga_setpack_cosine.csv
# Silhouette with euclidean
./exact_solution_setpack.py --lang pt --metric euclidean --save_log output_ga/std/exact_setpack_euclidean.csv
./ga_fs_setpack.py --lang pt --metric se --selec bin --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/std/ga_setpack_euclidean.csv
# Variance experiments
./exact_solution_setpack.py --lang pt --metric variance --save_log output_ga/std/exact_setpack_variance.csv
./ga_fs_setpack.py --lang pt --metric v --selec bin --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/std/ga_setpack_variance.csv
# Inertia experiments
./exact_solution_setpack.py --lang pt --metric inertia --save_log output_ga/std/exact_setpack_inertia.csv
./ga_fs_setpack.py --lang pt --metric i --selec bin --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose output_ga/std/ga_setpack_inertia.csv

