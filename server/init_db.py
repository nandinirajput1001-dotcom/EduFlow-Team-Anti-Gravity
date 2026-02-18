import sqlite3
import os

# Files ke naam
db_name = 'database.db'
schema_file = 'schema.sql'

print(f"🔄 Initializing database from {schema_file}...")

# Check karo ki schema.sql file wahin hai ya nahi
if not os.path.exists(schema_file):
    print(f"❌ Error: '{schema_file}' file nahi mili!")
    print("👉 Solution: Terminal mein 'cd server' type karo aur enter dabao, phir try karo.")
    exit(1)

try:
    # Database connect karo (agar nahi hai toh ban jayegi)
    connection = sqlite3.connect(db_name)
    
    # Schema read karke execute karo
    with open(schema_file) as f:
        connection.executescript(f.read())

    connection.commit()
    connection.close()

    print("\n✅ Database initialized successfully! (database.db ban gayi hai)")
    print("---------------------------------------------------")
    print("👤 Admin User:   admin@eduflow.edu  / adminpass2024")
    print("👤 Student User: student@eduflow.edu / password")
    print("---------------------------------------------------")

except Exception as e:
    print(f"\n❌ Something went wrong: {e}")