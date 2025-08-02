#!/usr/bin/env python3

from app.core.db import engine
import sqlalchemy as sa

with engine.connect() as conn:
    result = conn.execute(sa.text("SELECT id, email, name FROM \"user\" WHERE name IS NULL"))
    users = result.fetchall()
    print(f"Users with NULL names: {len(users)}")
    for user in users:
        print(f"  - ID: {user[0]}, Email: {user[1]}")
    
    # Also check for empty names
    result = conn.execute(sa.text("SELECT id, email, name FROM \"user\" WHERE name = ''"))
    users = result.fetchall()
    print(f"Users with empty names: {len(users)}")
    for user in users:
        print(f"  - ID: {user[0]}, Email: {user[1]}") 