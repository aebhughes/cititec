import unittest
import techtest as tt


class BasicTestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_parametercheck(self):
        u = tt.check_args(['pgm', 'username'])
        self.assertEqual(u, 'username')

    def test_api_call(self):
        d = tt.get_data('rj')
        t = d.get('recenttracks', None)
        self.assertNotEqual(t, None)
        track = t.get('track', None)
        self.assertNotEqual(track, None)
        d = tt.get_data('aebhughes')
        t = d.get('recenttracks', None)
        self.assertNotEqual(t, None)
        track = t.get('track', None)
        self.assertNotEqual(track, None)

    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()
