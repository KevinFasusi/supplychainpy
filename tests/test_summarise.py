import os
from operator import attrgetter
from unittest import TestCase

from decimal import Decimal

from supplychainpy import model_inventory
from supplychainpy.demand.summarise import OrdersAnalysis


class TestSummariseAnalysis(TestCase):
    def setUp(self):
        app_dir = os.path.dirname(__file__, )
        rel_path = 'supplychainpy/data2.csv'
        abs_file_path = os.path.abspath(os.path.join(app_dir, '..', rel_path))

        self.__skus = ['KR202-209', 'KR202-210', 'KR202-211']

        self.__orders_analysis = model_inventory.analyse_orders_abcxyz_from_file(file_path=abs_file_path,
                                                                                 z_value=Decimal(1.28),
                                                                                 reorder_cost=Decimal(5000),
                                                                                 file_type="csv",
                                                                                 length=12)
        self.__categories = ['excess_stock', 'shortages', 'average_orders']
        self.__analysis_summary = OrdersAnalysis(analysed_orders=self.__orders_analysis)

        self.__abc_raw = self.__analysis_summary.abc_xyz_raw

    def test_describe_sku_length(self):
        for description in self.__analysis_summary.describe_sku('KR202-209'):
            for items in description:
                self.assertEqual(21, len(items))

    def test_describe_type_error(self):
        with self.assertRaises(expected_exception=TypeError):
            for description in self.__analysis_summary.describe_sku('KR2-0'):
                print(description)

    # TODO-fix makes sure that all categories have are safe in this method
    def test_category_ranking_filter_top10(self):
        """Checks that the filter returns top ten shortages that are greater than the bottom ten.
            uses list of categories."""

        for category in self.__categories:
            top_ten = [item for item in
                       self.__analysis_summary.sku_ranking_filter(
                           attribute=category, count=10, reverse=True)]

            for item in top_ten:
                for bottom in [item for item in
                               self.__analysis_summary.sku_ranking_filter(
                                   attribute=category, count=10, reverse=False)]:
                    self.assertGreaterEqual(Decimal(item[category]), Decimal(bottom[category]))

    def test_category_ranking_filter_top10_attr_error(self):
        """ Tests the correct attribute name has been provided. Test uses shortage instead of shortages."""

        with self.assertRaises(expected_exception=AttributeError):
            top_ten_shortages = [item for item in
                                 self.__analysis_summary.sku_ranking_filter(
                                     attribute="shortage", count=10, reverse=True)]
            print(top_ten_shortages)

    def test_category_ranking_filter_bottom10(self):
        """Checks that the filter returns bottom ten of each category. Each value is compared against top ten for the
        same category."""
        for category in self.__categories:
            bottom_ten = [item for item in
                          self.__analysis_summary.sku_ranking_filter(
                              attribute=category, count=10, reverse=False)]

            for item in bottom_ten:
                for Top in [item for item in
                            self.__analysis_summary.sku_ranking_filter(
                                attribute=category, count=10, reverse=True)]:
                    self.assertLessEqual(Decimal(item[category]), Decimal(Top[category]))

    def test_abcxyz_category_selection(self):
        pass

    def test_abcxyz_classification_selection(self):
        for ay_summary in self.__analysis_summary.abc_xyz_summary(classification=('AY',)):
            for ay in ay_summary:
                self.assertEqual('AY', ay)

    def test_abcxyz_units_summary(self):
        pass

    def test_abcxyz_currency_summary(self):
        pass
