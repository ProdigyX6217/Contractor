from unittest import TestCase, main as unittest_main, mock
from bson.objectid import ObjectId

sample_ridepass_id = ObjectId('5d55cffc4a3d4031f42827a3')
sample_ridepass = {
    'title': 'Cat Videos',
    'description': 'Cats acting weird',
    'videos': [
        'https://youtube.com/embed/hY7m5jjJ9mM',
        'https://www.youtube.com/embed/CQ85sUNBK7w',
        'https://www.youtube.com/embed/8DPc2z9ZPDY'
    ]
}
sample_form_data = {
    'title': sample_ridepass['title'],
    'description': sample_ridepass['description'],
    'videos': '\n'.join(sample_ridepass['videos'])
}

class RidepassesTests(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_index(self):
        """Test the ridepasses homepage."""
        result = self.client.get('/')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Ridepass', result.data)

    def test_new(self):
        """Test the new ridepass creation page."""
        result = self.client.get('/ridepasses/new')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'New Ridepass', result.data)


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_show_playlist(self, mock_find):
        """Test showing a single ridepass."""
        mock_find.return_value = sample_ridepass

        result = self.client.get(f'/ridepasses/{sample_ridepass_id}')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)


    @mock.patch('pymongo.collection.Collection.find_one')
    def test_edit_ridepass(self, mock_find):
        """Test editing a single ridepass."""
        mock_find.return_value = sample_ridepass

        result = self.client.get(f'/ridepasses/{sample_ridepass_id}/edit')
        self.assertEqual(result.status, '200 OK')
        self.assertIn(b'Cat Videos', result.data)


    @mock.patch('pymongo.collection.Collection.insert_one')
    def test_submit_ridepass(self, mock_insert):
        """Test submitting a new ridepass."""
        result = self.client.post('/ridepasses', data=sample_form_data)

        # After submitting, should redirect to that ridepass's page
        self.assertEqual(result.status, '302 FOUND')
        mock_insert.assert_called_with(sample_ridepass)


    @mock.patch('pymongo.collection.Collection.update_one')
    def test_update_ridepass(self, mock_update):
        result = self.client.post(f'/ridepasses/{sample_ridepass_id}', data=sample_form_data)

        self.assertEqual(result.status, '302 FOUND')
        mock_update.assert_called_with({'_id': sample_ridepass_id}, {'$set': sample_ridepass})


    @mock.patch('pymongo.collection.Collection.delete_one')
    def test_delete_ridepass(self, mock_delete):
        form_data = {'_method': 'DELETE'}
        result = self.client.post(f'/ridepasses/{sample_ridepass_id}/delete', data=form_data)
        self.assertEqual(result.status, '302 FOUND')
        mock_delete.assert_called_with({'_id': sample_ridepass_id})


if __name__ == '__main__':
    unittest_main()
