from __future__ import print_function
import unittest
import techtest as tt
import os
import sys

class TextFile(unittest.TestCase):

    testData = '''\
123|Joking|Right Said Fred
456|Sugar Man|Rodregese
234|More Than A feeling|Boston
'''

    def setUp(self):
        self.tfile = open('testread.txt', 'w')
        self.tfile.write(self.testData)
        self.tfile.close()

    def test_file_create(self):
        t = tt.get_existing('testcreate')
        self.assertEqual(t, [])
        
    def test_file_read(self):
        t = tt.get_existing('testread')
        self.assertEqual(len(t), 3)

    def test_file_write(self):
        t = [(123,'Joking','Right Said Fred'),
             (456,'Sugar Man','Rodregus')]
        tt.write_existing(t, 'testwrite')
        t = tt.get_existing('testwrite')
        self.assertEqual(len(t), 2)        
        rec = t[0]
        for ndx, field in enumerate([123,'Joking','Right Said Fred']):
            self.assertEqual(rec[ndx], field)        


    def tearDown(self):
        pass

class TestResponse(unittest.TestCase):

    def test_get_data(self):
        r = tt.get_data('aebhughes')
        self.assertIn('recenttracks', r)
        d = r.get('recenttracks', None)
        self.assertNotEqual(d, None)
        t = d.get('track', None)
        self.assertNotEqual(t, None)
        one_t = t[0]
        self.assertIn('album', one_t)
        self.assertIn('name', one_t)
        self.assertIn('date', one_t)

    def test_create_rec(self):
        r = tt.get_data('aebhughes')
        cr = tt.create_rec(r)
        self.assertGreater(len(cr), 0)

    def test_get_recent_tracks(self):
        tt.get_recent_tracks('aebhughes')
        t = tt.get_existing('aebhughes')
        self.assertGreater(len(t), 0)

class TestResponse(unittest.TestCase):

    def test_display(self):
        tt.display_results('aebhughes')

if __name__ == '__main__':
    unittest.main()
