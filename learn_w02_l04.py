import sqlite3

conn = sqlite3.connect('emaildb.sqlite')
cur = conn.cursor()

cur.execute('Drop Table if exists Counts')

cur.execute('Create Table Counts (email Text, count Integer)')

fname = input('Enter file name: ')

if (len(fname) < 1):
    fname = 'mbox-short.txt'

fh = open(fname)
for line in fh:
    if not line.startswith('From: '):
        continue
    pieces = line.split()
    email = pieces[1]
    cur.execute('Select count from Counts where email = ?', (email, ))
    row = cur.fetchone()
    if row is None:
        cur.execute('Insert into Counts (email, count) values (?, 1)', (email, ))
    else:
        cur.execute('Update Counts Set count = count+1 where email = ?', (email,))

conn.commit()

sqlstr = 'Select email, count From Counts Order By count DESC Limit 10'

for row in cur.execute(sqlstr):
    print(str(row[0]), row[1])