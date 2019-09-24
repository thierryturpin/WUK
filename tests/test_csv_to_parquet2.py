import unittest
from pyspark.sql import SparkSession
from sparkscripts.csv_to_parquet_ref import mask_udf
from pyspark.sql.functions import lit
from pandas.util.testing import assert_frame_equal

class MyTest(unittest.TestCase):
    def test(self):

        spark = SparkSession.builder.appName("csv_to_parquet_test").getOrCreate()

        sample_file = spark.createDataFrame([('2018-05-31 00:00:00', '1:101:10104', 2, '20180601')], \
                                            ["timeslot", "dvbtriplet", "telespectateurs", "eventdatekey"])

        result_file = sample_file.select('timeslot', 'dvbtriplet', mask_udf('telespectateurs', lit(1)).alias('telespectateurs'),
                                         'eventdatekey')

        pd_sample_file = sample_file.toPandas()
        pd_result_file = result_file.toPandas()

        assert_frame_equal(pd_sample_file, pd_result_file)

        spark.stop()

if __name__ == '__main__':
    unittest.main()