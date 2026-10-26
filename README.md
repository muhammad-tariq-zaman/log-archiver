# log-archiver

Gzip-compress log files older than N days. Dry-run by default; pass
`--apply` to actually archive, and `--delete-original` to remove the source
after compression.

## How to run

```bash
python3 main.py --dir ./logs --days 30
python3 main.py --dir ./logs --days 30 --apply
```

## Example output (sample from test fixture data)

```text
would-archive: ./logs/old.log -> ./logs/old.log.gz
```

Standard library only. No network access.
