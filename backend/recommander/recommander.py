from pyspark.ml import PipelineModel
import pyspark.sql.functions as F
from pyspark.sql.types import DoubleType
import numpy as np
# conf = SparkConf()\
#     .setAppName("Recommandation System")\
#     .setMaster("local[*]")\
#     .set("spark.executor.memory", "3g")\
#     .set("spark.sql.shuffle.partitions", "100")\
#     .set("spark.executor.cores","2")\
#     .set("spark.executor.memory","3g")

# # Pass it to SparkSession
# spark = SparkSession.builder\
#     .config(conf=conf)\
#     .getOrCreate()



class Recommander:
    def __init__(self,spark,df_path,vectorizer_path,country,model_path=None):
        self.vectoried_df = spark.read.format("parquet").load(df_path).filter(F.array_contains(F.col("countries_tags"),country)).select("id","product_name_vec")
        self.model_1 = PipelineModel.load(model_path) if model_path else None
        self.spark = spark
        self.vectorizer  = PipelineModel.load(vectorizer_path)

    def suggest(self,df,max_):
        # Only for one input 
        if self.model_1:
            vec = self.__vectorise(df).head()[0]
            lsh = self.model_1.stages[-1]
            recommendations = lsh.approxNearestNeighbors(self.vectoried_df,vec, max_)
            return [ row['id'] for row in recommendations.select("id").collect()[:max_]]
        raise Exception("Model is not set")
    
    def cosine_similarity_with_query(self,df,vector_col,query_vector,ascending=False):
        def cosine_sim(v):
            arr1 = v.toArray()
            arr2 = query_vector.toArray()
            dot = float(np.dot(arr1, arr2))
            norm1 = float(np.linalg.norm(arr1))
            norm2 = float(np.linalg.norm(arr2))
            if norm1 == 0 or norm2 == 0:
                return 0.0
            return dot / (norm1 * norm2)
        cosine_sim_udf = F.udf(cosine_sim, DoubleType())
        df_with_sim = df.withColumn("cosine_similarity", cosine_sim_udf(F.col(vector_col)))
        sorted_df = df_with_sim.orderBy(F.col("cosine_similarity").asc() if ascending else F.col("cosine_similarity").desc())
        return [row ["id"] for row in sorted_df.collect()]
    def suggest_cosine(self,df,limit=10):
        n_ids = self.cosine_similarity_with_query(self.vectoried_df,"product_name_vec",df)[:limit]
        return n_ids

    
    def __vectorise(self,df):
        return self.vectorizer.transform(df).select("product_name_vec")
    
    def recommend_for_targets(self, target_vectors_df,top_n=5):
        recommondation = []
        vectorized_df = self.__vectorise(target_vectors_df)
        for row in vectorized_df.collect():
            recommondation.extend(self.suggest_cosine(row.product_name_vec,top_n))
        return list(set(recommondation))

  
    

    
# df = spark.createDataFrame([{"product_name":"Corn Flex"},{"product_name":"Yogurt"}])
# a = Recommander(spark,"./vectorized_df.parquet","./vectorizer","./similar")

# print(a.recommend_for_targets(df))
    
    


