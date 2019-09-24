import unittest
from pyspark.sql import SparkSession
from sparkscripts.csv_to_parquet_ref import mask_udf
from pyspark.sql.functions import lit
from pandas.util.testing import assert_frame_equal
import logging

class MyTest(unittest.TestCase):
    def test(self):

        logger = logging.getLogger('py4j')
        logger.setLevel(logging.WARN)

        mask_ratio = 2

        spark = SparkSession.builder.appName("csv_to_parquet_test").getOrCreate()

        sample_file = spark.createDataFrame([('2018-05-31 00:00:00', '1:101:10104', 2, '20180601')],
                                            ["timeslot", "dvbtriplet", "telespectateurs", "eventdatekey"])

        result_file = sample_file.select('timeslot', 'dvbtriplet', mask_udf('telespectateurs', lit(mask_ratio)).alias('telespectateurs'),
                                         'eventdatekey')

        expected_result_file = spark.createDataFrame([('2018-05-31 00:00:00', '1:101:10104', 4, '20180601')],
                                            ["timeslot", "dvbtriplet", "telespectateurs", "eventdatekey"])

        pd_result_file = result_file.toPandas()
        pd_expected_result_file = expected_result_file.toPandas()

        assert_frame_equal(pd_result_file, pd_expected_result_file)

        spark.stop()

if __name__ == '__main__':
    unittest.main()