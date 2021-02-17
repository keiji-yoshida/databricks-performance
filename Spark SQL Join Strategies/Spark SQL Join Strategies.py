# Databricks notebook source
# MAGIC %md
# MAGIC # Spark SQL Join Strategies

# COMMAND ----------

# MAGIC %md
# MAGIC ## Abstract

# COMMAND ----------

# MAGIC %md
# MAGIC A join strategy in Spark SQL is a way to process data in a Spark cluster to perform a table join. Understanding the characteristics of each join strategy is crucial for performance tuning of Spark jobs since the peformance of a Spark job differs hugely depending on a join strategy which is used in the job. This notebook describes a list of Spark SQL join strategies and the characteristics of each join strategy.

# COMMAND ----------

# MAGIC %md
# MAGIC ## List of Join Strategies

# COMMAND ----------

# MAGIC %md
# MAGIC 1. Shuffle-and-replicate nested loop join
# MAGIC 2. Shuffile Sort merge join
# MAGIC 3. Shuffle hash join
# MAGIC 4. Broadcast hash join / broadcast nested loop join

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. Shuffle-and-replicate Nested Loop Join

# COMMAND ----------

# MAGIC %md
# MAGIC ### Join Hints

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC SELECT /*+ SHUFFLE_REPLICATE_NL(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Description

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. Shuffle Sort Merge Join

# COMMAND ----------

# MAGIC %md
# MAGIC ### Join Hints

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC SELECT /*+ SHUFFLE_MERGE(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
# MAGIC SELECT /*+ MERGEJOIN(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
# MAGIC SELECT /*+ MERGE(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Description

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. Shuffle Hash Join

# COMMAND ----------

# MAGIC %md
# MAGIC ### Join Hints

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC SELECT /*+ SHUFFLE_HASH(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Description

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Broadcast Hash Join / Broadcast Nested Loop Join

# COMMAND ----------

# MAGIC %md
# MAGIC ### Join Hints

# COMMAND ----------

# MAGIC %md
# MAGIC ```sql
# MAGIC SELECT /*+ BROADCAST(t1) */ * FROM t1 INNER JOIN t2 ON t1.key = t2.key;
# MAGIC SELECT /*+ BROADCASTJOIN (t1) */ * FROM t1 LEFT JOIN t2 ON t1.key = t2.key;
# MAGIC SELECT /*+ MAPJOIN(t2) */ * FROM t1 RIGHT JOIN t2 ON t1.key = t2.key;
# MAGIC ```

# COMMAND ----------

# MAGIC %md
# MAGIC ### Description

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
# MAGIC ## Resources

# COMMAND ----------

# MAGIC %md
# MAGIC * [Join Strategy Hints for SQL Queries | Performance Tuning - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-queries)
# MAGIC * [Join Hints | Hints - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html#join-hints)
# MAGIC * [Tech Talk: Top Tuning Tips for Spark 3.0 and Delta Lake on Databricks - YouTube](https://www.youtube.com/watch?v=hcoMHnTcvmg)
# MAGIC * [Optimizing Apache Spark SQL Joins - Databricks](https://databricks.com/session/optimizing-apache-spark-sql-joins)