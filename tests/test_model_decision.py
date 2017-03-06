from unittest import TestCase

import logging

from supplychainpy.model_decision import analytical_hierarchy_process

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TestAnalyticalHierarchy(TestCase):
    def setUp(self):
        self.lorry_cost = {'scania': 55000, 'iveco': 79000, 'volvo': 59000, 'navistar': 66000}
        self.criteria = ('style', 'reliability', 'fuel_economy')
        self.criteria_scores = [(1, 1 / 2, 3), (0, 1, 4), (0, 0, 1)]
        self.options = ('scania', 'iveco', 'volvo', 'navistar')
        self.option_scores = {
            'reliability': [(1, 2, 5, 1), (1 / 2, 1, 3, 2), (1 / 5, 1 / 3, 1, 1 / 4), (1, 1 / 2, 4, 1)],
            'style': [(1, 1 / 4, 4, 1 / 6), (4, 1, 4, 1 / 4), (1 / 4, 1 / 4, 1, 1 / 5), (6, 4, 5, 1)],
            'fuel_economy': (62, 55, 56, 56)
        }
        self.lorry_decision = analytical_hierarchy_process(criteria=self.criteria, criteria_scores=self.criteria_scores,
                                                           options=self.options, option_scores=self.option_scores,
                                                           quantitative_criteria=('fuel_economy',),
                                                           item_cost=self.lorry_cost)

    def test_model_decision_ahp(self):
        best_choice = max(self.lorry_decision.get('analytical_hierarchy'),
                          key=lambda r: self.lorry_decision.get('analytical_hierarchy')[r])
        self.assertEqual('navistar', best_choice)

    def test_model_decision_cvb(self):
        best_choice = max(self.lorry_decision.get('analytical_hierarchy'),
                          key=lambda r: self.lorry_decision.get('cost_benefit_ratios')[r])
        self.assertEqual('scania', best_choice)
