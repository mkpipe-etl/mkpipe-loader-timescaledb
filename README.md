# mkpipe-loader-timescaledb

TimescaleDB loader plugin for [MkPipe](https://github.com/mkpipe-etl/mkpipe). Writes Spark DataFrames into TimescaleDB hypertables via PostgreSQL JDBC driver.

## Documentation

For more detailed documentation, please visit the [GitHub repository](https://github.com/mkpipe-etl/mkpipe).

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE](LICENSE) file for details.

---

## Connection Configuration

```yaml
connections:
  timescaledb_target:
    variant: timescaledb
    host: localhost
    port: 5432
    database: mydb
    schema: public
    user: myuser
    password: mypassword
```

---

## Table Configuration

```yaml
pipelines:
  - name: source_to_timescaledb
    source: my_source
    destination: timescaledb_target
    tables:
      - name: sensor_readings
        target_name: public.sensor_data
        replication_method: incremental
        batchsize: 10000
```

> **Note:** The target hypertable must exist before loading. TimescaleDB hypertables must be created with `create_hypertable()` before use.

---

## Write Parallelism & Throughput

```yaml
      - name: sensor_readings
        target_name: public.sensor_data
        replication_method: incremental
        batchsize: 10000
        write_partitions: 4
```

- **`batchsize`**: rows per JDBC batch `INSERT`. TimescaleDB routes inserts to the correct chunk automatically.
- **`write_partitions`**: reduces concurrent JDBC connections via `coalesce(N)`.

### Performance Notes

- TimescaleDB inserts are routed to chunks by the partition key (time column). Large batches that span many chunks can slow down inserts — moderate `batchsize` (5,000–20,000) is recommended.
- For high-throughput time-series ingestion, consider TimescaleDB's native [COPY protocol](https://docs.timescale.com/use-timescale/latest/ingest-data/) or the Timescale parallel copy tool outside of mkpipe.

---

## All Table Parameters

| Parameter | Type | Default | Description |
|---|---|---|---|
| `name` | string | required | Source table name |
| `target_name` | string | required | TimescaleDB destination hypertable name |
| `replication_method` | `full` / `incremental` | `full` | Replication strategy |
| `batchsize` | int | `10000` | Rows per JDBC batch insert |
| `write_partitions` | int | — | Coalesce DataFrame to N partitions before writing |
| `dedup_columns` | list | — | Columns used for `mkpipe_id` hash deduplication |
| `tags` | list | `[]` | Tags for selective pipeline execution |
| `pass_on_error` | bool | `false` | Skip table on error instead of failing |
