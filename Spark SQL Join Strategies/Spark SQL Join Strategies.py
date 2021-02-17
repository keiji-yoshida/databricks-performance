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
# MAGIC | **Shuffile Sort Merge Join**<br>`SELECT /*+ MERGE(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key` | Robust. Can handle any data size. Needs to shuffle and sort data, slower in most cases when the table size is small. |
# MAGIC | **Shuffle Hash Join**<br>`SELECT /*+ SHUFFLE_HASH(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;` | Needs to shuffle data but no sort. Can handle large tables, but will OOM too if data is skewed. One side is smallr (3x or more) and a partition of it can fit in memory. (Enable by `spark.sql.join.preferSortMergeJoin = false`)|
# MAGIC | **Broadcast Hash Join / Broadcast Nested Loop Join**<br>`SELECT /*+ BROADCAST(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;` | Requires one side to be small. No shuffle, no sort, very fast. |

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Shuffle-and-replicate Nested Loop Join

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

# MAGIC %md
# MAGIC ### Table Creation

# COMMAND ----------

# MAGIC %md
# MAGIC ### Clean-up

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resources

# COMMAND ----------

# MAGIC %md
# MAGIC * [Join Strategy Hints for SQL Queries | Performance Tuning - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-queries)
# MAGIC * [Join Hints | Hints - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html#join-hints)
# MAGIC * [Tech Talk: Top Tuning Tips for Spark 3.0 and Delta Lake on Databricks - YouTube](https://www.youtube.com/watch?v=hcoMHnTcvmg)
# MAGIC * [Optimizing Apache Spark SQL Joins - Databricks](https://databricks.com/session/optimizing-apache-spark-sql-joins)