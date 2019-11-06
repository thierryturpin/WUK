

CREATE EXTERNAL TABLE tweets_raw (
   id BIGINT,
   created_at STRING,
   source STRING,
   favorited BOOLEAN,
   retweet_count INT,
   retweeted_status STRUCT <
      text:STRING,
      id:STRING,
      `user`: STRUCT <screen_name:STRING,name:STRING>>,
   entities STRUCT <
      urls:ARRAY < STRUCT <expanded_url:STRING>>,
      user_mentions:ARRAY < STRUCT <screen_name:STRING,name:STRING>>,
      hashtags:ARRAY < STRUCT <text:STRING>>>,
   text STRING,
   `user` STRUCT <
      screen_name:STRING,
      id:STRING,
      name:STRING,
      friends_count:INT,
      followers_count:INT,
      statuses_count:INT,
      verified:BOOLEAN,
      utc_offset:STRING,
      time_zone:STRING,
      geo_enabled:BOOLEAN,
      lang:STRING,
      location:STRING>,
    place STRUCT <
      country:STRING,
      country_code:STRING,
      full_name:STRING,
      name:STRING,
      place_type:STRING>,
   in_reply_to_screen_name STRING )
ROW FORMAT  serde 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://micropoledih/tweets/';