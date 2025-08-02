#!/usr/bin/env python3

from app.core.db import engine
import sqlalchemy as sa

with engine.connect() as conn:
    result = conn.execute(sa.text("SELECT column_name FROM information_schema.columns WHERE table_name = 'user' ORDER BY ordinal_position"))
    columns = [row[0] for row in result]
    print("Current user table columns:")
    for col in columns:
        print(f"  - {col}") 