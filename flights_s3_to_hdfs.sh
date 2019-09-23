#!/bin/bash

mkdir data
cd data
aws s3 sync s3://micropoledih/DIS/ .

hadoop fs -mkdir /user/hadoop/csv/

YEAR=1998

while [  $YEAR -le 2008 ]; do
  echo Handling $YEAR

  bzip2 -d $YEAR.csv.bz2
  hadoop fs -copyFromLocal $YEAR.csv /user/hadoop/csv/
  rm $YEAR.csv

  let YEAR=YEAR+1
done

echo ALL DONE!

