'''
Use this file to test database functioning correctly
'''
import sqlite3

#Turn the results from the database into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# test that the cascade on delete works
# get the competition name
conn = sqlite3.connect('survivor.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute("SELECT * \
    FROM ParticipatingUser")
initial = c.fetchall()

print("Current set of ParticipatingUsers:")
# print out each user and email
for user in initial:
    print("   -", user['user_nm']) #, user['email'])

# delete BigJase from the CompUser table and see if the he exists in the Participating user table
print('\nDeleting BigJase from the CompUser table\n')
conn = sqlite3.connect('survivor.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute("pragma foreign_keys=on;")
c.execute("DELETE \
        FROM CompUser \
        WHERE user_nm like '%jas%';")
conn.commit()

# Query the CompUser table again and print the result
conn = sqlite3.connect('survivor.db')
conn.row_factory = dict_factory
c = conn.cursor()
c.execute("SELECT * \
    FROM ParticipatingUser")
updated = c.fetchall()
print('Updated set of ParticipatingUsers:')
for user in updated:
    print("   -", user['user_nm'])
