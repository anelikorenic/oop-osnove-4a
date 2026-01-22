import sqlite3


def inicijalizacija():
    conn = sqlite3.connect('Imenik.db')
    cur = conn.cursor()

    sql = """CREATE TABLE IF NOT EXISTS Kontakti (id INTEGER PRIMARY KEY AUTOINCREMENT, ime_prezime TEXT NOT NULL, broj_mobitela TEXT NOT NULL);"""

    cur.execute(sql)
    conn.commit()
    conn.close()


def unesi_kontakt():
    ime = input('Unesi ime i prezime: ')
    broj = input('Unesi broj mobitela: ')

    conn = sqlite3.connect('Imenik.db')
    cur = conn.cursor()

    sql = 'INSERT INTO Kontakti (ime_prezime, broj_mobitela) VALUES (?, ?)'
    cur.execute(sql, (ime, broj))

    conn.commit()
    conn.close()

    print('Kontakt dodan!')


def ispisi_kontakte():
    conn = sqlite3.connect('Imenik.db')
    cur = conn.cursor()

    cur.execute('SELECT * FROM Kontakti')
    rezultati = cur.fetchall()

    print('\n--- TELEFONSKI IMENIK ---')
    print('{:<5} | {:<25} | {}'.format('ID', 'IME I PREZIME', 'BROJ'))
    print('-'*50)

    for red in rezultati:
        print("{:<5} | {:<25} | {}".format(red[0], red[1], red[2]))


    conn.close()

def obrisi_kontakt():
    ispisi_kontakte()
    kontakt_id = input('\nUnesi ID kontakta za brisanje: ')

    conn = sqlite3.connect('Imenik.db')
    cur = conn.cursor()

    sql = 'DELETE FROM Kontakti WHERE id = ?'
    cur.execute(sql, (kontakt_id, ))

    if cur.rowcount > 0:
        print('Kontakt obrisan.')
    else:
        print('Kontakt s tim ID-em ne postoji.')

    conn.commit()
    conn.close()


inicijalizacija()

while True:
    print('TELEFONSKI IMENIK')
    print('1. Unesi novi kontakt')
    print('2. Ispisi sve kontakte')
    print('3. Obrisi kontakt')
    print('4. Izlaz')

    izbor = input('Odaberi opciju (1-4): ')

    if izbor == '1':
        unesi_kontakt()

    elif izbor == '2':
        ispisi_kontakte()

    elif izbor == '3':
        obrisi_kontakt()

    elif izbor == '4':
        print('Izlaz')
        break

    else:
        print('Nepostojeća opcija, pokušajte ponovo.')

