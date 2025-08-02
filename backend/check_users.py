#!/usr/bin/env python3

from app.core.db import engine
import sqlalchemy as sa

with engine.connect() as conn:
    result = conn.execute(sa.text("SELECT id, email, name, id_troy FROM \"user\" LIMIT 5"))
    users = result.fetchall()
    print("Existing users:")
    for user in users:
        print(f"  - ID: {user[0]}, Email: {user[1]}, Name: {user[2]}, Troy ID: {user[3]}") 