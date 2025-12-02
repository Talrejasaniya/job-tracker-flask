import sqlite3
conn=sqlite3.connect('database/data.db')
c=conn.cursor()
c.execute(
    '''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
    '''
)

c.execute(
    '''
    CREATE TABLE IF NOT EXISTS applications(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company_name TEXT NOT NULL,
        role TEXT NOT NULL,
        status TEXT,
        date_applied TEXT,
        user_id  INTEGER,
        FOREIGN KEY (user_id) REFERENCES users(id)
    )
    '''
)
print("Tables created successfully.")
conn.commit()
conn.close()