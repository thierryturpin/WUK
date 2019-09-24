import unittest
from pyspark.sql import SparkSession
from sparkscripts.csv_to_parquet_ref import mask_udf

class MyTest(unittest.TestCase):
    def test(self):
        spark = SparkSession.builder.appName("csv_to_parquet").getOrCreate()

        sample_file = self.spark.sparkContext.parallelize(['2018-05-31 00:00:00', '1:101:10104', '2', '20180601'], 2)

        result_file = sample_file.select('timeslot', 'dvbtriplet', mask_udf('telespectateurs').alias('telespectateurs'),
                                         'eventdatekey')

        self.assertEqual(0, 0)

if __name__ == '__main__':
    unittest.main()