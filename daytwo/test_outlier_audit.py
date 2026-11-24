
"""Add at least three meaningful tests."""
import unittest
import pandas as pd
from outlier_audit import audit_data


class TestOutlierAudit(unittest.TestCase):

    def test_missing_columns(self):
        data = pd.DataFrame({
            "sample_id": ["WINE-001"],
            "alcohol": [14.23]
        })

        with self.assertRaises(ValueError):
            audit_data(data)

    def test_zero_variance_columns(self):
        data = pd.DataFrame({
            "sample_id": ["WINE-001", "WINE-002", "WINE-003"],
            "alcohol": [14.0, 14.0, 14.0],
            "malic_acid": [2.0, 2.0, 2.0],
            "color_intensity": [5.0, 5.0, 5.0],
            "proline": [500.0, 500.0, 500.0],
            "target": [0, 0, 0]
        })

        results = audit_data(data)

        self.assertFalse(results["retained"]["malic_acid_z_flag"].any())
        self.assertFalse(results["retained"]["proline_z_flag"].any())
        self.assertEqual(len(results["quarantined"]), 0)

    def test_quarantine_only_invalid_domain_records(self):
        data = pd.DataFrame({
            "sample_id": ["WINE-001", "WINE-002", "WINE-003",
                          "WINE-004", "WINE-005", "WINE-006"],
            "alcohol": [14.0, 13.0, 12.0, 13.5, 14.5, 13.2],
            "malic_acid": [1.0, 1.0, 1.0, 1.0, 99.0, 1.5],
            "color_intensity": [5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            "proline": [100.0, 100.0, 100.0, 100.0, 100.0, -45.0],
            "target": [0, 0, 0, 1, 1, 1]
        })

        results = audit_data(data)

        self.assertEqual(len(results["quarantined"]), 1)
        self.assertEqual(
            results["quarantined"].iloc[0]["sample_id"],
            "WINE-006"
        )

        retained_outlier = results["retained"][
            results["retained"]["sample_id"] == "WINE-005"
        ]

        self.assertEqual(len(retained_outlier), 1)
        self.assertTrue(retained_outlier.iloc[0]["review_needed"])
        self.assertTrue(retained_outlier.iloc[0]["malic_acid_iqr_flag"])


if __name__ == "__main__":
    unittest.main()
