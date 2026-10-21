import unittest
from loader import *

class TestLoader(unittest.TestCase):
    """Tests for looking up locations with loader.py."""
    def setUp(self):
        """Create one geolocator for every test."""
        self.geolocator = get_geolocator()


    def test_valid_locations(self):
        """Known places should return the right coordinates and type."""
        expected = [
            ("Museum of Modern Art", 40.7618552, -73.9782438, "Museum"),
            ("USS Alabama Battleship Memorial Park",
             30.684373, -88.015316, "Park"),
        ]
        names = [row[0] for row in expected]
        df = build_geo_dataframe(names, self.geolocator)
        self.assertEqual(len(df), len(expected))
        for i, (name, lat, lon, loc_type) in enumerate(expected):
            row = df.iloc[i]
            self.assertEqual(row["location"], name)
            self.assertAlmostEqual(row["latitude"], lat, delta=0.01)
            self.assertAlmostEqual(row["longitude"], lon, delta=0.01)
            self.assertEqual(row["type"], loc_type)
        return None


    def test_invalid_location(self):
        """A fake place should keep its name and have NA everywhere else."""
        result = fetch_location_data(self.geolocator, "asdfqwer1234")
        self.assertEqual(result["location"], "asdfqwer1234")
        self.assertTrue(pd.isna(result["latitude"]))
        self.assertTrue(pd.isna(result["longitude"]))
        self.assertTrue(pd.isna(result["type"]))


if __name__ == "__main__":
    unittest.main()
    
