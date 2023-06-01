from app.db import DatabaseManager
import subprocess

DB_NAME = './db.sqlite3'


class TestDBManager:
    def test_add_select(self):
        # cleanup before testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

        d = DatabaseManager(DB_NAME)
        columns = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'title': 'TEXT NOT NULL',
                'url': 'TEXT NOT NULL',
                'notes': 'TEXT',
                'date_added': 'TEXT NOT NULL',
                }
        d.create_table('bookmarks', columns)
        data = {
                'title': 'my first bookmark',
                'url': 'http://adhysetiawan.com',
                'notes': 'a very good website',
                'date_added': '1 June 2023',
                }
        d.add('bookmarks', data)
        res = d.select('bookmarks').fetchall()
        print(res)
        assert len(res) == 1

        # cleanup after testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

    def test_add_delete_select(self):
        # cleanup before testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

        d = DatabaseManager(DB_NAME)
        columns = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'item': 'TEXT NOT NULL',
                }
        d.create_table('bookmarks', columns)
        data = {
                'item': 'some random item',
                }
        d.add('bookmarks', data)
        delete_entry = {'id': 1}
        d.delete('bookmarks', delete_entry)
        res = d.select('bookmarks').fetchall()
        print(res)
        assert len(res) == 0

        # cleanup after testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

    def test_one_add_multiple_delete(self):
        # cleanup before testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

        d = DatabaseManager(DB_NAME)
        columns = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'item': 'TEXT NOT NULL',
                }
        d.create_table('bookmarks', columns)
        data = {
                'item': 'some random item',
                }
        d.add('bookmarks', data)
        delete_entry = {'id': 1}
        d.delete('bookmarks', delete_entry)
        d.delete('bookmarks', delete_entry)
        d.delete('bookmarks', delete_entry)
        d.delete('bookmarks', delete_entry)
        res = d.select('bookmarks').fetchall()
        print(res)
        assert len(res) == 0

        # cleanup after testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

    def test_add_delete_add(self):
        # cleanup before testing
        subprocess.call(f'rm {DB_NAME}', shell=True)

        d = DatabaseManager(DB_NAME)
        columns = {
                'id': 'INTEGER PRIMARY KEY AUTOINCREMENT',
                'item': 'TEXT NOT NULL',
                }
        d.create_table('bookmarks', columns)
        data = {
                'item': 'some random item',
                }
        d.add('bookmarks', data)
        delete_entry = {'id': 1}
        d.delete('bookmarks', delete_entry)
        d.add('bookmarks', data)
        res = d.select('bookmarks').fetchall()
        print(res)
        assert len(res) == 1

        # cleanup after testing
        subprocess.call(f'rm {DB_NAME}', shell=True)
