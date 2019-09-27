# WUK
demo EMR and codepipeline [build status](https://codebuild.eu-west-1.amazonaws.com/badges?uuid=eyJlbmNyeXB0ZWREYXRhIjoiSVNrcWorUUpmeFZqbmxMZHRTYzJWSnhrNndDQkJsYURET3RjczJoeVU5SDZLVHF3dmtxdkZ1OGgyVENoRUVlNlM1elNjM3dPdTlrb2JtYW5oWExQZFRnPSIsIml2UGFyYW1ldGVyU3BlYyI6IlhKU1UxOGpyMW1ITm1oL2QiLCJtYXRlcmlhbFNldFNlcmlhbCI6MX0%3D&branch=master)


Not using the `--auto-terminate \`  

```bash
myEMR="$(aws emr create-cluster --auto-scaling-role EMR_AutoScaling_DefaultRole \
                       --applications Name=Hadoop Name=Spark Name=Hive\
                       --tags 'Name=EMR' \
                       --ec2-attributes '{"KeyName":"thierryturpin","InstanceProfile":"EMR_EC2_DefaultRole","ServiceAccessSecurityGroup":"sg-cb4309af","SubnetId":"subnet-c167d1a4","EmrManagedSlaveSecurityGroup":"sg-ca4309ae","EmrManagedMasterSecurityGroup":"sg-c94309ad"}' \
                       --service-role EMR_DefaultRole \
                       --enable-debugging \
                       --release-label emr-5.26.0 \
                       --log-uri 's3n://aws-logs-662050823481-eu-west-1/elasticmapreduce/' \
                       --name 'EMR1' \
                       --instance-groups '[{"InstanceCount":1,"InstanceGroupType":"MASTER","InstanceType":"c5.2xlarge","Name":"Master - 1"},{"InstanceCount":2,"InstanceGroupType":"CORE","InstanceType":"c5.2xlarge","Name":"Core - 2"}]' \
                       --region eu-west-1 \
                       --bootstrap-action Path="s3://micropoledih/emr_bootstrap_codepipeline.sh" | jq -r ".ClusterId" )"; echo $myEMR

watch -d "aws emr describe-cluster --cluster-id $myEMR | jq -r ".Cluster.Status.State""

```

For a new cluster trigger the code deploy

```
aws codepipeline start-pipeline-execution --name wuk
```

Checking status
```
aws codepipeline get-pipeline-state --name wuk | jq -c '.stageStates[] | select(.stageName | . and contains("Deploy")).latestExecution.status'
```

Watch status of the cluster
```bash
watch -d "aws emr describe-cluster --cluster-id $myEMR | jq -r ".Cluster.Status.State""
```

Add step to cluster

```bash
aws emr add-steps --cluster-id $myEMR \
                  --steps Type=Spark,Name="csv_to_parquet",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--conf,spark.yarn.appMasterEnv.PYSPARK_PYTHON=python36,--conf,spark.executorEnv.PYSPARK_PYTHON=python36,/home/hadoop/sparkscripts/csv_to_parquet_ref.py,-cs3n://dih2018/extract_audiences.csv,-d/home/hadoop/sparkscripts/csv_to_parquet.yml]

```

Spark-submit
```
spark-submit --deploy-mode cluster --conf spark.yarn.appMasterEnv.PYSPARK_PYTHON=python34 --conf spark.executorEnv.PYSPARK_PYTHON=python34 /Users/thierryturpin/PycharmProjects/WUK/sparkscripts/csv_to_parquet.py -c s3://micropoledih/DiDi.yml

```

## To debug
```bash
yarn logs -applicationId application_1516525003387_0014
``