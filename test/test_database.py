from unittest import TestCase

from gphotos.LocalData import LocalData
from test_setup import SetupDbAndCredentials


# noinspection SqlResolve
class DatabaseTest(TestCase):
    def test_new_schema(self):
        s = SetupDbAndCredentials()
        # get a single file
        args = ['--drive-file', '20170102_094337.jpg',
                '--skip-picasa']
        s.test_setup('new_schema', args=args, trash_files=True)
        s.gp.start(s.parsed_args)

        db = LocalData(s.root)
        db.cur.execute(
            'UPDATE Globals SET Version = "1.0" WHERE Id IS 1')
        db.store()
        db.con.close()

        s.test_setup('new_schema', args=args)
        s.gp.start(s.parsed_args)

        db = LocalData(s.root)
        db.cur.execute('SELECT Version From Globals WHERE Id IS 1')
        version = float(db.cur.fetchone()[0])
        self.assertEqual(version, LocalData.VERSION)

        db.cur.execute(
            'UPDATE Globals SET Version = "100.0" WHERE Id IS 1')
        db.store()

        with self.assertRaises(ValueError):
            s.test_setup('new_schema', args=args)
