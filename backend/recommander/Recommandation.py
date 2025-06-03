
from recommander.recommander import Recommander
from pyspark import SparkConf
from pyspark.sql import SparkSession
class Recommandation :
    def __init__(self,country,vectors_path="/home/aes-saouiqui/spark-project/backend/vectorized_df.parquet",vectorizer_path="/home/aes-saouiqui/spark-project/backend/vectorizer",model_path=None):
        conf = SparkConf()\
                .setAppName("Recommandation System")\
                .setMaster("local[*]")\
                .set("spark.executor.memory", "3g")\
                .set("spark.sql.shuffle.partitions", "100")\
                .set("spark.executor.cores","2")\
                .set("spark.executor.memory","3g")
        # Pass it to SparkSession
        self.spark = SparkSession.builder\
    .config(conf=conf)\
    .getOrCreate()
    
        self.recommander = Recommander(self.spark,vectors_path,vectorizer_path,country,model_path)
    
    def recommand(self,recipe:list,top_n:5):
        data = list(map(lambda x : {"product_name":x},recipe))
        df = self.spark.createDataFrame(data)
        return self.recommander.recommend_for_targets(df,top_n)
    

# a = Recommandation("./vectorized_df.parquet","./vectorizer","./similar")

