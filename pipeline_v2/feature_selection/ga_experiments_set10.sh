#!/bin/bash

# Using all database
# Silhouette with cosine
# Basic mutation
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_01.csv
echo "Finished execution 01 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_02.csv
echo "Finished execution 02 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_03.csv
echo "Finished execution 03 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_04.csv
echo "Finished execution 04 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_05.csv
echo "Finished execution 05 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_06.csv
echo "Finished execution 06 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_07.csv
echo "Finished execution 07 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_08.csv
echo "Finished execution 08 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_09.csv
echo "Finished execution 09 - basic mutation"
./ga_fs_setpack_new_mut.py --lang pt --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_10.csv
echo "Finished execution 10 - basic mutation"

# Extended mutation
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_01.csv
echo "Finished execution 01 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_02.csv
echo "Finished execution 02 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_03.csv
echo "Finished execution 03 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_04.csv
echo "Finished execution 04 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_05.csv
echo "Finished execution 05 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_06.csv
echo "Finished execution 06 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_07.csv
echo "Finished execution 07 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_08.csv
echo "Finished execution 08 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_09.csv
echo "Finished execution 09 - extended mutation"
./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 6 output_ga/all/ga_setpack_cosine_new_mut_10.csv
echo "Finished execution 10 - extended mutation"

./ga_fs_setpack_new_mut.py --lang pt --muttype 0.1 --metric sc --selec bin --db all --save_log --ngen 300 --pop 50 --mincxpb 0.8 --elsize 0.5 --mutpb 0.02 --divfac 0.5 --verbose --corr_threshold 0.7 --maxs 36 --mins 2 output_ga/all/ga_setpack_cosine_superheavy.csv
echo "Finished execution of superheavy test"
