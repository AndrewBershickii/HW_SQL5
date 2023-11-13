import psycopg2


def print_bd(cur):
    cur.execute('''
                SELECT * FROM clients AS c JOIN phones AS p ON c.id=p.client_id;
                ''')
    db=cur.fetchall()
    for i in db:
        print(f'id: {i[0]}, first_name: {i[1]}, last_name: {i[2]}, email: {i[3]}, phone: {i[6]}')

def create_db(cur):
    cur.execute('''
                CREATE TABLE IF NOT EXISTS clients(
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(30) NOT NULL,
                last_name VARCHAR(30) NOT NULL,
                email VARCHAR(50) NOT NULL UNIQUE
                );
                ''')
    conn.commit()
    cur.execute('''
                CREATE TABLE IF NOT EXISTS phones(
                id SERIAL PRIMARY KEY,
                client_id INTEGER REFERENCES clients(id),
                phone BIGINT NOT NULL UNIQUE
                );
                ''')
    conn.commit()

def add_client(cur, first_name, last_name, email, phone=None):
    cur.execute('''
                INSERT INTO clients(first_name, last_name, email)
                VALUES(%s, %s, %s) RETURNING id;
                ''', (first_name, last_name, email))
    conn.commit()
    id=cur.fetchone()
    if phone != None:
        cur.execute('''
                    INSERT INTO phones(phone, client_id)
                    VALUES (%s, %s);
                    ''', (phone, id))
    conn.commit()

def add_phone(cur, client_id, phone):
    cur.execute('''
                INSERT INTO phones(client_id, phone)
                VALUES(%s, %s);
                ''', (client_id, phone))
    conn.commit()

def change_client(cur, client_id, first_name=None, last_name=None, email=None, phone=None, old_phone=None):
    if first_name != None:
        cur.execute('''
                    UPDATE clients 
                    SET first_name=%s 
                    WHERE id=%s;
                    ''', (first_name, client_id))
        conn.commit()
    if last_name != None:
        cur.execute('''
                    UPDATE clients 
                    SET last_name=%s 
                    WHERE id=%s;
                    ''', (last_name, client_id))
        conn.commit()
    if email != None:
        cur.execute('''
                    UPDATE clients 
                    SET email=%s 
                    WHERE id=%s;
                    ''', (email, client_id))
        conn.commit()
    if phone != None and client_id and old_phone != None:
        cur.execute('''
                    SELECT id FROM phones
                    WHERE client_id=%s AND phone=%s;
                    ''', (client_id, old_phone))
        phone_id = cur.fetchall()[0][0]
        cur.execute('''
                    UPDATE phones
                    SET phone=%s
                    WHERE id=%s;
                    ''', (phone, phone_id))
        conn.commit()

def delete_phone(cur, client_id, phone):
    cur.execute('''
                SELECT id FROM phones
                WHERE client_id=%s AND phone=%s;
                ''', (client_id, phone))
    del_id=cur.fetchall()[0][0]
    cur.execute('''
                DELETE FROM phones
                WHERE id=%s;
                ''', (del_id,))
    conn.commit()

def delete_client(cur, client_id):
    cur.execute('''
                DELETE FROM phones
                WHERE client_id=%s;
                ''', (client_id,))
    conn.commit()
    cur.execute('''
                DELETE FROM clients
                WHERE id=%s;
                ''', (client_id,))
    conn.commit()

def find_client(cur, id=None, first_name=None, last_name=None, email=None, phone=None):
    cur.execute('''
                SELECT c.id, c.first_name, c.last_name, c.email, p.phone
                FROM clients AS c
                JOIN phones AS p 
                ON c.id = p.client_id
                WHERE c.id=%s
                OR c.first_name=%s
                OR c.last_name=%s
                OR c.email=%s
                OR p.phone=%s;
                ''', (id, first_name, last_name, email, phone))
    result=cur.fetchall()
    for n in result:
        print(f'id: {n[0]}, first_name: {n[1]}, last_name: {n[2]}, email: {n[3]}, phone: {n[4]}')


with psycopg2.connect(database="clients", user="postgres", password="123") as conn:
    with conn.cursor() as cur:
        cur.execute('''
                    DROP TABLE phones CASCADE;
                    DROP TABLE clients CASCADE;
                    ''')
        create_db(cur)
        add_client(cur, 'Andrew', 'Bersh', 'AB@mail.ru', 1111)
        add_phone (cur, 1, 2222)
        add_client(cur, 'Test', 'Test', 'Test@test.test')
        add_phone(cur, 2, 9999)
        change_client(cur, 2, 'Change', phone=9876, old_phone=9999)
        # delete_phone(cur, 1, 2222)
        # delete_client(cur, 2)
        # print_bd(cur)
        find_client(cur, 1)