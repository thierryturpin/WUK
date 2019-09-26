
## Create Hive external table (before loading data to HDFS)

With the hive client

```
create table flights_csv (
 Year INT,
 Month INT,
 DayofMonth INT,
 DayOfWeek INT,
 DepTime varchar(4),
 CRSDepTime varchar(4),
 ArrTime varchar(4),
 CRSArrTime varchar(4),
 UniqueCarrier char(2),
 FlightNum varchar(4),
 TailNum varchar(10),
 ActualElapsedTime char(5),
 CRSElapsedTime char(5),
 AirTime char(5),
 ArrDelay char(5),
 DepDelay char(5),
 Origin char(3),
 Dest char(3),
 Distance INT,
 TaxiIn char(4),
 TaxiOut char(4),
 Cancelled char(1),
 CancellationCode char(2),
 Diverted char(1),
 CarrierDelay char(4),
 WeatherDelay char(4),
 NASDelay char(4),
 SecurityDelay char(4),
 LateAircraftDelay char(4)
 )
 ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS TEXTFILE
LOCATION '/user/hadoop/csv/'
tblproperties ("skip.header.line.count"="1");

create table flights_prq stored as parquet as select * from flights_csv;
```

## Start Spark Thirft server
```
cd /usr/lib/spark/sbin
sudo /usr/lib/spark/sbin/start-thriftserver.sh --master yarn-client 
```

## Start beeline

# to-do make query before cache and after cache and compare

```
!connect jdbc:hive2://localhost:10001
select count(*) as count, year, origin from flights_prq where origin = 'ORD' group by year, origin;
cache table flights_prq;
```

