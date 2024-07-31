python run.py --engines milvus-cloud-default --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin.txt  2>&1 

--skip-upload
python run.py --skip-upload --engines milvus-cloud-default --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin-more.txt  2>&1 

python run.py --skip-upload --engines milvus-cloud-2nd --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin-more-second.txt  2>&1 

python run.py --skip-upload --engines milvus-cloud-no-recall --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin-more-no-recall.txt  2>&1 


# queries 1x-load
python run.py --skip-upload --engines milvus-cloud-query-1x-load --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin-query-1x-load.txt  2>&1 

# queries 1x
python run.py --skip-upload --engines milvus-cloud-query-1x --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin-query-1x.txt  2>&1 

# queries 10x
python run.py --skip-upload --engines milvus-cloud-query-10x --datasets dbpedia-openai-1M-1536-angular --host "in01-71e00c68e0cd56d.aws-us-west-2.vectordb.zillizcloud.com" > /home/ec2-user/dbpedia-openai-1M-1536-angular-tianmin-query-10x.txt  2>&1 


## redis
# 1x-load
python run.py --engines redis-m-32-ef-256-1x-load --datasets dbpedia-openai-1M-1536-angular

# 1x
python run.py --skip-upload --engines redis-m-32-ef-256-1x --datasets dbpedia-openai-1M-1536-angular
