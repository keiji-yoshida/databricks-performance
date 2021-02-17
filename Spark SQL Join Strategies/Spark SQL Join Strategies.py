# Databricks notebook source
# MAGIC %md
# MAGIC # Spark SQL Join Strategies

# COMMAND ----------

# MAGIC %md
# MAGIC Databricks Runtime Version: 7.6 ML (includes Apache Spark 3.0.1, Scala 2.12)

# COMMAND ----------

# MAGIC %md
# MAGIC ## Abstract

# COMMAND ----------

# MAGIC %md
# MAGIC A join strategy in Spark SQL is a way to process data in a Spark cluster to perform a table join. Understanding the characteristics of each join strategy is crucial for performance tuning of Spark jobs since the peformance of a Spark job differs hugely depending on a join strategy which is used in the job. This notebook describes a list of Spark SQL join strategies and the characteristics of each join strategy.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Resources

# COMMAND ----------

# MAGIC %md
# MAGIC * [Join Strategy Hints for SQL Queries | Performance Tuning - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-performance-tuning.html#join-strategy-hints-for-sql-queries)
# MAGIC * [Join Hints | Hints - Spark 3.0.1 Documentation](https://spark.apache.org/docs/latest/sql-ref-syntax-qry-select-hints.html#join-hints)
# MAGIC * [Tech Talk: Top Tuning Tips for Spark 3.0 and Delta Lake on Databricks - YouTube](https://www.youtube.com/watch?v=hcoMHnTcvmg)
# MAGIC * [Optimizing Apache Spark SQL Joins - Databricks](https://databricks.com/session/optimizing-apache-spark-sql-joins)