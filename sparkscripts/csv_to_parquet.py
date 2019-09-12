# -*- coding: UTF-8 -*-
import argparse
import os
import logging
import yaml
from pyspark.sql.types import *
from pyspark.sql.functions import udf
from pyspark.sql import SparkSession

def mask_func(mask_value):
    masked_value = mask_value * mask_ratio
    return masked_value

mask_udf = udf(mask_func, LongType())


def set_validate_env():
    SPARK_HOME = os.environ.get('SPARK_HOME', None)
    JAVA_HOME = os.environ.get('JAVA_HOME', None)
    HADOOP_HOME = os.environ.get('HADOOP_HOME', None)
    logging.info('Spark: {} '.format(SPARK_HOME))
    logging.info('Java: {} '.format(JAVA_HOME))
    logging.info('Hadoop: {} '.format(HADOOP_HOME))


def set_logging():
    logging.basicConfig(filename='csv_to_parquet.log',
                        filemode='w',
                        level=logging.INFO,
                        format='[%(asctime)s] - %(message)s',
                        datefmt='%Y-%m-%dT%H:%M:%S')

def get_param(param):
    parser = argparse.ArgumentParser(description='DiDi2')
    parser.add_argument('-c', dest='csv_file', required=True)
    parser.add_argument('-d', dest='conf_file', required=True)
    args = parser.parse_args()
    if param == 'csv_file':
        return args.csv_file
    elif param == 'conf_file':
        return args.conf_file

if __name__ == '__main__':
    global mask_ratio

    set_logging()
    logging.info('################################################--START--################################################')
    logging.info('PID: {}'.format(os.getpid()))

    with open(get_param('conf_file')) as configfile:
        configdata = yaml.load(configfile)

    mask_ratio = configdata['ratio']

    csv_file = get_param('csv_file')

    bucket = csv_file.split('//')[1].split('/')[0]
    key = csv_file.split('//')[1].split('/')[1]

    set_validate_env()

    spark = SparkSession.builder.appName("csv_to_parquet").getOrCreate()
    logging.info('Spark UI: {}'.format(spark.sparkContext.uiWebUrl))
    logging.info('Spark parallelism: {}'.format(spark.sparkContext.defaultParallelism))
    logging.info('Spark master: {}'.format(spark.sparkContext.master))
    logging.info('Invoked with configuration file: {}'.format(get_param('conf_file')))

    sample_file = spark.read.csv(csv_file,
                                 header=True,
                                 sep=';',
                                 encoding='UTF-8',
                                 inferSchema=True)

    logging.info('Number of lines in file: {}'.format(sample_file.count()))

    result_file = sample_file.select('timeslot', 'dvbtriplet', mask_udf('telespectateurs').alias('telespectateurs'),
                                     'eventdatekey')

    parquet_file = csv_file + '.prq'
    parquet_file = parquet_file.replace('*', '__WILDCARD__')
    parquet_file = parquet_file.replace('IN', 'OUT')

    result_file.write.parquet(parquet_file, mode='overwrite', compression='none')


    spark.stop()
    logging.info('################################################---END---################################################')
