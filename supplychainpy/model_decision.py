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

from supplychainpy.bi._analytical_heirachy_process import _PairwiseComparison


def analytical_hierarchy_process(criteria: tuple, criteria_scores: list, options: tuple, option_scores: dict,
                                 quantitative_criteria: tuple = None, **kwargs):
    """ Compute an analytical hierarchy for alternative choices based on relative weights and priorities of categories.

    Args:
        criteria (tuple):                List the criteria to base decision between alternative choices.
        criteria_scores (list):          List the scores for the criteria as a list of tuples, the reciprocals are
                                         auto-calculated.
        options (tuple):                 The alternative otpions to decide between.
        option_scores (dict):            A dict of tuples scoring the alternatives. The tuple order must mirror the
                                         'alternative' argument tuple.
        quantitative_criteria (tuple):   List the quantitative criteria e.g. 'fuel economy', that use representative
                                         values and not scores
        **kwargs:
            item_cost (dict):   A dict of alternatives and their corresponding costs. Only necessary if seeking to use cost benefit ratios for further discretion.

    Returns:
        dict:   Summary of analytical hierarchy and cost benefit analysis if kwargs 'item_cost' used.

    Examples:

    >>> lorry_cost = {'scania': 68000,'iveco': 79000,'volvo': 59000,'navistar': 66000}
    >>> criteria = ('style', 'reliability', 'fuel_economy')
    >>> criteria_scores = [(1, 1 / 2, 3), (0, 1, 4), (0, 0, 1)]
    >>> options = ('scania', 'iveco', 'volvo', 'navistar')
    >>> options_scores ={'reliability': [(1, 2, 5, 1), (1 / 2, 1, 3, 2), (1 / 5, 1 / 3, 1, 1 / 4), (1, 1 / 2, 4, 1)],
    ...     'style': [(1, 1 / 4, 4, 1 / 6), (4, 1, 4, 1 / 4),(1 / 4, 1 / 4, 1, 1 / 5), (6, 4, 5, 1)],
    ...     'fuel_economy': (62, 55, 56, 56)}
    >>> lorry_decision = analytical_hierarchy_process(criteria= criteria, criteria_scores=criteria_scores,
    ...     options= options, option_scores=options_scores, quantitative_criteria=('fuel_economy',),
    ...     item_cost = lorry_cost)

    """
    ahp = _PairwiseComparison(criteria=criteria,
                              criteria_scores=criteria_scores,
                              options=options,
                              option_scores=option_scores,
                              quantitative_criteria=quantitative_criteria)
    if kwargs:
        ahp_cvb = ahp.cost_benefit_summary(ahp_summary=ahp.summary(), item_cost=kwargs.get('item_cost'))
        return {'analytical_hierarchy': ahp.summary(), 'cost_benefit_ratios': ahp_cvb}

    return ahp.summary()
