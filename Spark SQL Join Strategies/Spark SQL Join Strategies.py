# Databricks notebook source
# MAGIC %md
# MAGIC # Spark SQL Join Strategies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Abstract

# COMMAND ----------

# MAGIC %md
# MAGIC A join strategy in Spark SQL is a way to process data in a Spark cluster to perform a table join. Understanding the characteristics of each join strategy is crucial for performance tuning of Spark jobs since the peformance of a Spark job differs hugely depending on a join strategy which is used in the job. This notebook describes the characteristics of each join strategy.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Summary

# COMMAND ----------

# MAGIC %md
# MAGIC | Join Strategy | Characteristics |
# MAGIC | ------------- | --------------- |
# MAGIC | **1. Shuffle-and-replicate Nested Loop Join**<br>`SELECT /*+ SHUFFLE_REPLICATE_NL(t1) */ * FROM t1 INNER JOIN t2` | Does not require join keys as it is a cartesian product of the tables. Avoid doing this if you can. |
# MAGIC | **2. Shuffile Sort Merge Join**<br>`SELECT /*+ MERGE(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key` | Robust. Can handle any data size. Needs to shuffle and sort data, slower in most cases when the table size is small. |
# MAGIC | **3. Shuffle Hash Join**<br>`SELECT /*+ SHUFFLE_HASH(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;` | Needs to shuffle data but no sort. Can handle large tables, but will OOM too if data is skewed. One side is smallr (3x or more) and a partition of it can fit in memory. (Enable by `spark.sql.join.preferSortMergeJoin = false`)|
# MAGIC | **4. Broadcast Hash Join / Broadcast Nested Loop Join**<br>`SELECT /*+ BROADCAST(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;` | Requires one side to be small. No shuffle, no sort, very fast. |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Shuffle-and-replicate Nested Loop Join

# COMMAND ----------

# MAGIC %md
# MAGIC Cartesian product of two tables is calculated in this join strategy.

# COMMAND ----------

# MAGIC %md
# MAGIC <img src="https://raw.githubusercontent.com/keiji-yoshida/databricks-performance/main/Spark%20SQL%20Join%20Strategies/imgs/Shuffle-and-replicate_nested_loop_join_overview.png" width="800px" />

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Shuffle Sort Merge Join

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Shuffle Hash Join

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Broadcast Hash Join / Broadcast Nested Loop Join

# COMMAND ----------

# MAGIC %md
# MAGIC ## Demo

# COMMAND ----------

# MAGIC %md
# MAGIC ### Databricks Runtime Version

# COMMAND ----------

# MAGIC %md
# MAGIC 7.6 ML (includes Apache Spark 3.0.1, Scala 2.12)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Preparation

# COMMAND ----------

import re

# Get and process the user's name.
username_raw = dbutils.notebook.entry_point.getDbutils().notebook().getContext().tags().apply('user')
username = re.sub('[^A-Za-z0-9]+', '', username_raw).lower()

# Generate a temporary database name.
# Re-create and use the database.
database_name = f"dbperfdemo_{username}"
spark.sql(f"drop database if exists {database_name} cascade")
spark.sql(f"create database {database_name}")
spark.sql(f"use {database_name}")
print(f"database_name: {database_name}")

# Generate a Delta Lake tables' root path.
# Remove the path.
delta_path = f"/tmp/{database_name}"
dbutils.fs.rm(delta_path, True)
print(f"delta_path: {delta_path}")

# COMMAND ----------

# DBTITLE 1,Create t10k table which has 10k records.
spark.sql(f"""
  create or replace table t10k
  using delta
  location '{delta_path}/t10k'
  as
  select
    value
  , cast(value as string) as key
  from
    (select explode(sequence(1, 10000)) as value)
""")

display(spark.sql("describe detail t10k"))

# COMMAND ----------

# DBTITLE 1,Create t50k table which has 50k records.
spark.sql(f"""
  create or replace table t50k
  using delta
  location '{delta_path}/t50k'
  as
  select
    value
  , cast(value as string) as key
  from
    (select explode(sequence(1, 50000)) as value)
""")

display(spark.sql("describe detail t50k"))

# COMMAND ----------

# DBTITLE 1,Create t100k table which has 100k records.
spark.sql(f"""
  create or replace table t100k
  using delta
  location '{delta_path}/t100k'
  as
  select
    value
  , cast(value as string) as key
  from
    (select explode(sequence(1, 100000)) as value)
""")

display(spark.sql("describe detail t100k"))

# COMMAND ----------

# DBTITLE 1,Create t10m table which has 10m records.
spark.sql(f"""
  create or replace table t10m
  using delta
  location '{delta_path}/t10m'
  as
  select
    value
  , cast(value as string) as key
  from
    (select explode(sequence(1, 10000000)) as value)
""")

display(spark.sql("describe detail t10m"))

# COMMAND ----------

# DBTITLE 1,Create t50m table which has 50m records.
spark.sql(f"""
  create or replace table t50m
  using delta
  location '{delta_path}/t50m'
  as
  select
    value
  , cast(value as string) as key
  from
    (select explode(sequence(1, 50000000)) as value)
""")

display(spark.sql("describe detail t50m"))

# COMMAND ----------

# DBTITLE 1,Create t100m table which has 100m records.
spark.sql(f"""
  create or replace table t100m
  using delta
  location '{delta_path}/t100m'
  as
  select
    value
  , cast(value as string) as key
  from
    (select explode(sequence(1, 100000000)) as value)
""")

display(spark.sql("describe detail t100m"))

# COMMAND ----------

# DBTITLE 1,Create t1b table which has 1b records.
spark.sql(f"""
  create or replace table t1b
  using delta
  location '{delta_path}/t1b'
  as
  select
    value
  , cast(value as string) as key
  from
    (
      select
        t.value + (100000000 * v.v) as value
      from
        t100m t
          inner join
            (select explode(sequence(0, 9)) as v) v
    )
""")

spark.sql("optimize t1b zorder by (key)")

display(spark.sql("describe detail t1b"))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Shuffle-and-replicate Nested Loop Join vs Broadcast Nested Loop Join

# COMMAND ----------

# MAGIC %md
# MAGIC #### Shuffle-and-replicate Nested Loop Join

# COMMAND ----------

# Set `spark.sql.autoBroadcastJoinThreshold` and `spark.databricks.adaptive.autoBroadcastJoinThreshold` to 0b
# so that shuffle-and-replicate nested loop join will be chosen as a join strategy.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "0b")
spark.conf.set("spark.databricks.adaptive.autoBroadcastJoinThreshold", "0b")

display(spark.sql("""
select
  sum(t1.value + t2.value)
from
  t50k t1
    inner join
      t50k t2
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC **Shuffle-and-replicate nested loop join** was chosen as a join strategy. It took about **3 minutes** to complete the query execution.

# COMMAND ----------

# MAGIC %md
# MAGIC <img src="https://github.com/keiji-yoshida/databricks-performance/raw/main/Spark%20SQL%20Join%20Strategies/imgs/Shuffle-and-replicate_nested_loop_join.png" />

# COMMAND ----------

# MAGIC %md
# MAGIC #### Broadcast Nested Loop Join

# COMMAND ----------

# Set `spark.sql.autoBroadcastJoinThreshold` and `spark.databricks.adaptive.autoBroadcastJoinThreshold` to 10mb
# so that broadcast nested loop join will be chosen as a join strategy.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10mb")
spark.conf.set("spark.databricks.adaptive.autoBroadcastJoinThreshold", "10mb")

display(spark.sql("""
select
  sum(t1.value + t2.value)
from
  t50k t1
    inner join
      t50k t2
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC **Broadcast nested loop join** was chosen as a join strategy. It took about **20 seconds** to complete the query execution.

# COMMAND ----------

# MAGIC %md
# MAGIC <img src="https://raw.githubusercontent.com/keiji-yoshida/databricks-performance/main/Spark%20SQL%20Join%20Strategies/imgs/Broadcast_nested_loop_join.png" />

# COMMAND ----------

# MAGIC %md
# MAGIC ### Shuffile Sort Merge Join vs Shuffle Hash Join vs Broadcast Hash Join

# COMMAND ----------

# MAGIC %md
# MAGIC #### Shuffile Sort Merge Join

# COMMAND ----------

# Set `spark.sql.autoBroadcastJoinThreshold` and `spark.databricks.adaptive.autoBroadcastJoinThreshold` to 0b and `spark.sql.join.preferSortMergeJoin` to true
# so that shuffle sort merge join will be chosen as a join strategy.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "0b")
spark.conf.set("spark.databricks.adaptive.autoBroadcastJoinThreshold", "0b")
spark.conf.set("spark.sql.join.preferSortMergeJoin", "true")

display(spark.sql("""
select 
  sum(t1b.value + t10k.value)
from
  t1b
    inner join
      t10k
    on
      t1b.key = t10k.key
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC #### Shuffle Hash Join

# COMMAND ----------

# Set `spark.sql.autoBroadcastJoinThreshold` and `spark.databricks.adaptive.autoBroadcastJoinThreshold` to 0b and `spark.sql.join.preferSortMergeJoin` to true
# so that shuffle sort merge join will be chosen as a join strategy.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "0b")
spark.conf.set("spark.databricks.adaptive.autoBroadcastJoinThreshold", "0b")
spark.conf.set("spark.sql.join.preferSortMergeJoin", "false")

display(spark.sql("""
select /*+ shuffle_hash(t1b) */ 
  sum(t1b.value + t10k.value)
from
  t1b
    inner join
      t10k
    on
      t1b.key = t10k.key
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC #### Broadcast Hash Join

# COMMAND ----------

# Set `spark.sql.autoBroadcastJoinThreshold` and `spark.databricks.adaptive.autoBroadcastJoinThreshold` to 0b and `spark.sql.join.preferSortMergeJoin` to true
# so that shuffle sort merge join will be chosen as a join strategy.
spark.conf.set("spark.sql.autoBroadcastJoinThreshold", "10mb")
spark.conf.set("spark.databricks.adaptive.autoBroadcastJoinThreshold", "10mb")

display(spark.sql("""
select 
  sum(t1b.value + t10k.value)
from
  t1b
    inner join
      t10k
    on
      t1b.key = t10k.key
"""))

# COMMAND ----------

# MAGIC %md
# MAGIC ### Clean-up

# COMMAND ----------

# Drop the database and its tables.
spark.sql(f"drop database {database_name} cascade")

# Remove the Delta Lake tables' root path.
dbutils.fs.rm(delta_path, True)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resources

# COMMAND ----------

# MAGIC %md
# MAGIC * [Join Strategy Hints for SQL Queries | Performance Tuning - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-queries)
# MAGIC * [Join Hints | Hints - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html#join-hints)
# MAGIC * [Tech Talk: Top Tuning Tips for Spark 3.0 and Delta Lake on Databricks - YouTube](https://www.youtube.com/watch?v=hcoMHnTcvmg)
# MAGIC * [Optimizing Apache Spark SQL Joins - Databricks](https://databricks.com/session/optimizing-apache-spark-sql-joins)