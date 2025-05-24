import mysql.connector
from datetime import datetime, timedelta
import time
import random
DB_CONFIG = {
    "host": "localhost",  # Change if using a remote DB
    "user": "root",
    "password": "1234567890",
    "database": "test"  # Choose your schema
}
conn = mysql.connector.connect(**DB_CONFIG)
cursor = conn.cursor()

# Create the orders table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_date DATE NOT NULL,
        user_id INT NOT NULL,
        location_id VARCHAR(10) NOT NULL,
        payment_id INT UNIQUE NULL,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (location_id) REFERENCES locations(id) ON DELETE CASCADE,
        FOREIGN KEY (payment_id) REFERENCES payments(id) ON DELETE SET NULL
    )
""")
conn.commit()

# Fetch IDs
cursor.execute("SELECT id FROM users")
user_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM locations")
location_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT id FROM payments")
all_payment_ids = [row[0] for row in cursor.fetchall()]
random.shuffle(all_payment_ids)

# First 800 orders get unique payment_ids, remaining 200 get NULL
payment_ids_for_orders = all_payment_ids[:800] + [None] * 200
random.shuffle(payment_ids_for_orders)
print(payment_ids_for_orders)
# Generate 1000 order rows
orders = []
for i in range(1000):
    order_date = (datetime.today() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d')
    user_id = random.choice(user_ids)
    location_id = random.choice(location_ids)
    payment_id = payment_ids_for_orders[i]
    orders.append((order_date, user_id, location_id, payment_id))

print('here')
insert_query = """
    INSERT INTO orders (order_date, user_id, location_id, payment_id)
    VALUES (%s, %s, %s, %s)
"""
batch_size = 100  # Insert in chunks of 100 rows

for i in range(0, len(orders), batch_size):
    batch = orders[i:i + batch_size]
    cursor.executemany(insert_query, batch)
    print(f'''in batch {i}''')
    conn.commit()  # Commit after each batch to release locks
    time.sleep(0.5)


cursor.close()
conn.close()
print("✅ Successfully inserted 1000 orders with unique payment_ids!")