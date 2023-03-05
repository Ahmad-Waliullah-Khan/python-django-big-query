from django.test import TestCase
from unittest.mock import patch, MagicMock

from ad.tasks import pause_ad, unpause_ad, update_ad


class AdTestCase(TestCase):
    @patch("ad.tasks.fetch_ads")
    @patch("ad.tasks.pause_ad")
    def test_pause_ad(self, mock_pause_ad, mock_fetch_ads):
        # Create a mock context object
        mock_context = MagicMock()
        # Add assertions here
        # Set up mock data for fetch_ads
        ad1 = MagicMock(id=1)
        ad2 = MagicMock(id=2)
        mock_fetch_ads.return_value = [ad1, ad2]

        # Call the pause_ad task
        pause_ad(client=None, ad_id=1)
        pause_ad(client=None, ad_id=2)

        # Check that pause_ad was called twice with the correct ad IDs
        mock_pause_ad.assert_any_call(None, 1)
        mock_pause_ad.assert_any_call(None, 2)

    @patch("ad.tasks.fetch_ads")
    @patch("ad.tasks.unpause_ad")
    def test_unpause_ad(self, mock_unpause_ad, mock_fetch_ads):
         # Create a mock context object
        mock_context = MagicMock()
        # Set up mock data for fetch_ads
        ad1 = MagicMock(id=1)
        ad2 = MagicMock(id=2)
        mock_fetch_ads.return_value = [ad1, ad2]

        # Call the unpause_ad task
        unpause_ad(client=None, ad_id=1)
        unpause_ad(client=None, ad_id=2)

        # Check that unpause_ad was called twice with the correct ad IDs
        mock_unpause_ad.assert_any_call(None, 1)
        mock_unpause_ad.assert_any_call(None, 2)

    @patch("ad.tasks.fetch_ads")
    @patch("ad.tasks.update_ad")
    def test_update_ad(self, mock_update_ad, mock_fetch_ads):
         # Create a mock context object
        mock_context = MagicMock()
        # Set up mock data for fetch_ads
        ad1 = MagicMock(id=1)
        ad2 = MagicMock(id=2)
        mock_fetch_ads.return_value = [ad1, ad2]

        # Call the update_ad task
        update_ad(client=None, ad_id=1, attribute1="New Headline 1", attribute2="New Description 1")
        update_ad(client=None, ad_id=2, attribute1="New Headline 2", attribute2="New Description 2")

        # Check that update_ad was called twice with the correct ad IDs and attributes
        mock_update_ad.assert_any_call(None, 1, "New Headline 1", "New Description 1")
        mock_update_ad.assert_any_call(None, 2, "New Headline 2", "New Description 2")
