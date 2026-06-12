---
name: database-operations
description: Guide for interacting with the system's PostgreSQL database using the DBManager interface, covering key tables and common patterns.
version: 1.0.0
---

# Database Operations

## Golden Rule

**Data goes in the database. No random CSVs/JSON outside `data/` directory.**
- JSON/CSV = raw, unclean, not for production
- PostgreSQL = production data storage

## DBManager Interface

```python
from db_manager import DBManager, default_db

# Use default connection
df = default_db.fetch_df("SELECT * FROM unified_games WHERE sport = 'nba'")

# Or create custom connection
db = DBManager(connection_string="postgresql://user:pass@host:5432/db")
```

## Key Tables

| Table | Purpose |
|-------|---------|
| `unified_games` | All games across sports |
| `game_odds` | Kalshi/sportsbook odds |
| `placed_bets` | Bet history and results |
| `elo_ratings` | Historical Elo snapshots |
| `portfolio_snapshots` | Portfolio value over time |

## Common Operations

### Fetch as DataFrame
```python
df = default_db.fetch_df("""
    SELECT * FROM unified_games
    WHERE sport = :sport AND game_date >= :start_date
""", {"sport": "nba", "start_date": "2024-01-01"})
```

### Execute Query
```python
default_db.execute("""
    UPDATE placed_bets SET status = 'won'
    WHERE bet_id = :bet_id
""", {"bet_id": "123"})
```

### Insert DataFrame
```python
df.to_sql("unified_games", default_db.get_engine(),
          if_exists="append", index=False)
```

### Upsert Pattern
```python
default_db.execute("""
    INSERT INTO game_odds (game_id, source, yes_price)
    VALUES (:game_id, :source, :yes_price)
    ON CONFLICT (game_id, source)
    DO UPDATE SET yes_price = EXCLUDED.yes_price
""", params)
```

## Connection Defaults

From environment or docker-compose:
- Host: `localhost`
- Port: `5432`
- User: `airflow`
- Password: `airflow`
- Database: `airflow`

## Data Validation

Always validate before commits:

```python
from data_validation import validate_nba_data

report = validate_nba_data()
if not report.is_valid:
    raise ValueError(f"Validation failed: {report.errors}")
```

## Files to Reference

- `plugins/db_manager.py` - DBManager class
- `plugins/data_validation.py` - Validation utilities
- `plugins/database_schema_manager.py` - Schema definitions
