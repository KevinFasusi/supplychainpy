# Copyright (c) 2015-2016, The Authors and Contributors
# <see AUTHORS file>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the
# following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the
# following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote
# products derived from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE
# USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

from copy import deepcopy

import numpy as np


class _PairwiseComparison:
    __UNKNOWN = "unknown"
    __RANDOM_INDICES = {1:0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.51}

    def __init__(self, criteria: tuple, criteria_scores: list, options: tuple, option_scores: dict,
                 quantitative_criteria: tuple = None):
        self._criteria = criteria
        self._importance = criteria_scores
        self._alternatives = options
        self._alternative_scores = option_scores
        self._quantitative_criteria = quantitative_criteria
        self._cr = self._consistency_ratio()

    @property
    def criteria(self) -> tuple:
        return self._criteria

    @criteria.setter
    def criteria(self, criteria: tuple):
        self._criteria = criteria

    @property
    def importance(self) -> list:
        return self._importance

    @importance.setter
    def importance(self, importance: list):
        self._importance = importance

    @property
    def alternatives(self) -> tuple:
        return self._alternatives

    @alternatives.setter
    def alternatives(self, alternatives: tuple):
        self._alternatives = alternatives

    @property
    def alternative_scores(self) -> dict:
        return self._alternative_scores

    @alternative_scores.setter
    def alternative_scores(self, alternative_scores: dict):
        self._alternative_scores = alternative_scores

    @property
    def quantitative_criteria(self) -> tuple:
        return self._quantitative_criteria

    @quantitative_criteria.setter
    def quantitative_criteria(self, quantitative_criteria: tuple):
        self.quantitative_criteria = quantitative_criteria

    @property
    def consistency_ratio(self):
        return self._cr

    def _map_reciprocal(self, importance_score: list) -> np.array:
        """ Fills in the reciprocal relative weights matrix of  for each criterion.

        Args:
            importance_score:   The relative scores for each criterion.

        Returns:
            np.array:           A matrix of scores indicating the relative importance of the criterion.
        """
        importance_score_matrix = np.array(importance_score)
        for index_one, score_one in enumerate(importance_score):
            for index_two, score_two in enumerate(importance_score):
                if index_two >= index_one:
                    importance_score_matrix[index_two, index_one] = self._reciprocal(
                        importance_score_matrix[index_one, index_two])
        return importance_score_matrix

    def summary(self) -> dict:
        """ Summaries the Analytical Hierarchy Process,with a dict of scores for ranking.

        Returns:
            dict:   Scores for each alternative based on the relative importance of each category.
        """
        np.set_printoptions(precision=3, suppress=True)
        criteria_eigenvector_rank = self.compute_criteria_eingenvector()
        alternative_matrix_subjective = {val: self._square_matrix(np.array(self.alternative_scores.get(val))) for val in
                                         self.alternative_scores.keys() if val not in self.quantitative_criteria}

        alternative_matrix_eigenvectors = self._alternative_eigenvector(alternative_matrix_subjective)
        alternative_matrix_quantitative = self._normalise_quantitative_rank()

        recompile_main_hierarchy_matrix = self._recompile_main_hierarchy_matrix(alternative_matrix_eigenvectors,
                                                                                alternative_matrix_quantitative)

        ahp_solution = self._compile_ahp_solution(recompiled_main_hierarchy=recompile_main_hierarchy_matrix,
                                                  criteria_eigenvector=criteria_eigenvector_rank)
        return ahp_solution

    @staticmethod
    def cost_benefit_summary(ahp_summary: dict, item_cost: dict) -> dict:
        """ Normalises the costs for each alternative and converts cost into benefits cost ratio.

        Args:
            ahp_summary (dict):     Summary of analytical hierarchy.
            item_cost (dict):       Cost of each alternative

        Returns:
            dict:   benefit cost ratio for alternatives in analytical hierarchy

        """
        if ahp_summary.keys() == item_cost.keys():
            total_cost = sum([item_cost.get(i) for i in item_cost])
            normalised_item_cost = {}
            for i in item_cost:
                normalised_item_cost.update({i: item_cost.get(i) / total_cost})
            cost_benefit_ratios = {}
            for i in normalised_item_cost:
                cost_benefit_ratios.update({i: ahp_summary.get(i) / normalised_item_cost.get(i)})
            return cost_benefit_ratios
        else:
            raise KeyError("Please check keys and ensure both 'ahp_summary' and 'item_costs' have identical keys.")

    def _compile_ahp_solution(self, recompiled_main_hierarchy: dict, criteria_eigenvector: tuple) -> dict:
        """ Multiplies the criteria rankings by the rankings for the alternatives.

        Args:
            recompiled_main_hierarchy (dict):   The eignenvectors for the subjective and objective categories
            criteria_eigenvector (dict):        The eigenvector for the criteria.

        Returns:
            dict:   The final solution for the AHP.

        """
        ahp_solution = {}
        stack = []
        for count, alternative in enumerate(self.alternatives):
            for index, name in enumerate(self.criteria):
                stack.append(recompiled_main_hierarchy.get(name)[count] * criteria_eigenvector[index])
            ahp_solution.update({alternative: sum(stack)})
            stack.clear()
        return ahp_solution

    def _alternative_eigenvector(self, alternative_matrix):
        """

        Args:
            alternative_matrix:

        Returns:

        """
        np.set_printoptions(precision=3, suppress=True)
        eigenvectors_for_alternatives = []
        for x in alternative_matrix.keys():
            eigenvectors_for_alternatives.append({x: self._calculate_eigenvector(alternative_matrix.get(x))})
        return eigenvectors_for_alternatives

    def _normalise_quantitative_rank(self) -> list:
        """ Normalises the values for the categories ranked using quantities e.g. fuel consumption.

        Returns:
            list:   Normalised ranking of alternatives for quantitative categories.

        """
        normalised_quantitive_criteria_ranking = []
        for x in self.quantitative_criteria:
            quant_criteria = self.alternative_scores.get(x)
            sum_quant_criteria = sum(quant_criteria)
            normalised_quantitive_criteria = tuple([i / sum_quant_criteria for i in quant_criteria])
            normalised_quantitive_criteria_ranking.append({x: normalised_quantitive_criteria})
        return normalised_quantitive_criteria_ranking

    @staticmethod
    def _recompile_main_hierarchy_matrix(alternative_matrix_quantitative: list,
                                         alternative_matrix_eigenvectors: list) -> dict:
        """ Combines the subjective matrices and the objective (quantitative) matrices together.

        Args:
            alternative_matrix_quantitative (list):     Eignevectors for the objective categories for the AHP
            alternative_matrix_eigenvectors (list):     Eignevectors for the subjective categories for the AHP

        Returns:
            dict:   Combined subjective and objective eignevectors.

        """
        for i in alternative_matrix_quantitative:
            alternative_matrix_eigenvectors.append(i)
        recompiled_matrix = {}
        for x in alternative_matrix_eigenvectors:
            recompiled_matrix.update(x)
        return recompiled_matrix

    @staticmethod
    def _reciprocal(first_score: float) -> float:
        return 1 / first_score

    @staticmethod
    def _square_matrix(score: np.array) -> np.array:
        """ Matrix multiplication

        Args:
            score: completed scores for comparison matrix

        Returns:
            np.array:   squared completed scores for comparison matrix

        """
        return score * score

    def _calculate_eigenvector(self, squared_comparison_matrix: np.array) -> tuple:
        """ Calculates the eigenvector.

        Args:
            squared_comparison_matrix (np.array):   Squared comparison matrix.

        Returns:
            tuple:  Eigenvector.

        """

        sum_block = [sum(i) for i in squared_comparison_matrix]
        block_total = sum(sum_block)
        eigenvector = [i / block_total for i in sum_block]
        last_result = eigenvector

        while True:

            new_matrix = self._square_matrix(squared_comparison_matrix)
            sum_block = [sum(i) for i in new_matrix]
            block_total = sum(sum_block)
            new_eigenvector = [i / block_total for i in sum_block]
            if new_eigenvector == last_result:
                break
            else:
                last_result = deepcopy(new_eigenvector)
                new_eigenvector.clear()
        # comparison_eigenvector = namedtuple('comparison_eigenvector', [*self.criteria])
        # final_eigenvector = comparison_eigenvector(*eigenvector)
        return tuple(eigenvector)

    def compute_criteria_eingenvector(self) -> tuple:
        """ Initiates and conducts the calculation of eigenvectors.

        Returns:
            tuple: Eigenvector.

        """
        if self._criteria != self.__UNKNOWN and self._importance != self.__UNKNOWN:
            if isinstance(self._criteria, tuple):
                comparison = self.pairwise_tp(score=self._importance)
                squared_comparison_matrix = self._square_matrix(score=comparison)
                eigenvector_ranking = self._calculate_eigenvector(squared_comparison_matrix=squared_comparison_matrix)
                return eigenvector_ranking
            else:
                raise TypeError("The criteria supplied as an argument is an incorrect type. "
                                "Please supply a correct type.")
        else:
            raise KeyError("Please supply criteria and importance.")

    def pairwise_tp(self, score: list) -> tuple:
        """ Creates the comparison matrix by filling in the reciprocal values.

        Args:

            score (list):   Scores for criteria

        Returns:
            tuple:  completed comparisons.

        """
        comparison_matrix = self._map_reciprocal(importance_score=score)
        return comparison_matrix

    def _consistency_ratio(self):
        """ Calculates the consistency ratio, indicating how consistent the decision maker is being with their pair-wise
        comparisons.

        Returns:
            float:  Consistency ratio indicating the consistency of the pair-wise comparison.

        """
        comparison = self.pairwise_tp(score=self._importance)
        squared_comparison_matrix = self._square_matrix(score=comparison)
        eigenvector_ranking = self._calculate_eigenvector(squared_comparison_matrix=squared_comparison_matrix)
        sum_comparison = np.sum(squared_comparison_matrix, axis=0)
        lambda_max = sum(sum_comparison * np.array(eigenvector_ranking))
        consistency_index = (lambda_max - len(self.criteria)) / (len(self.criteria) - 1)
        consistency_ratio = consistency_index / self.__RANDOM_INDICES.get(len(self.criteria))
        return consistency_ratio

