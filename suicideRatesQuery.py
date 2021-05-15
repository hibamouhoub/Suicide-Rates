import findspark
findspark.init('/home/hiba/spark-3.1.1-bin-hadoop3.2')
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.sql.types import StructType,StringType,IntegerType,DoubleType

spark = SparkSession.builder.master("local").appName('Suicide Rates').getOrCreate()

schema = StructType() \
      .add("country",StringType(),True) \
      .add("year",IntegerType(),True) \
      .add("sex",StringType(),True) \
      .add("age",StringType(),True) \
      .add("suicides_no",IntegerType(),True) \
      .add("population",IntegerType(),True) \
      .add("suicides/100k pop",DoubleType(),True) \
      .add("HDI_for_year",DoubleType(),True) \
      .add("gdp_for_year ($)",StringType(),True) \
      .add("gdp_per_capita ($)",IntegerType(),True) \
      .add("generation",StringType(),True)

data = spark.read \
    .options(header='True', inferSchema='True', delimiter=',')\
    .schema(schema) \
    .csv("master.csv")

data.registerTempTable('data')
sqlContext = SQLContext(spark)

year = input('\n\nPlease select a year from 1986 to 2015: \n')
country = input('Please enter a country: \n')

dff1 = sqlContext\
    .sql("SELECT SUM(suicides_no) AS numberof_suicides from data WHERE year="+year+" AND country='"+country+"'")\
    .toPandas()
print('Total Number of Suicides: ',dff1.numberof_suicides[0])


