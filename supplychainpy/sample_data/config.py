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

import os

APP_DIR = os.path.dirname(__file__, )
COMPLETE_CSV_SM = 'complete_dataset_small.csv'
COMPLETE_CSV_XSM = 'complete_dataset_xsmall.csv'
COMPLETE_CSV_LG = 'complete_dataset_large'
PARTIAL_COL_CSV_SM ='partial_dataset_col_small.csv'
PARTIAL_ROW_TXT_SM = 'partial_dataset_row_small.txt'
PARTIAL_COL_TXT_SM = 'partial_dataset_col_small.txt'
PARTIAL_CSV_SM = 'partial_dataset_small.csv'
FORECAST_PICKLE = '../sample_data/forecast.pickle'
RECOMMENDATION_PICKLE = '../sample_data/recommendation.pickle'
PROFILE_PICKLE = '../sample_data/profile.pickle'

ABS_FILE_PATH = {'COMPLETE_CSV_SM': os.path.abspath(os.path.join(APP_DIR, COMPLETE_CSV_SM)),
                 'PARTIAL_ROW_TXT_SM': os.path.abspath(os.path.join(APP_DIR, PARTIAL_ROW_TXT_SM)),
                 'COMPLETE_CSV_LG': os.path.abspath(os.path.join(APP_DIR, COMPLETE_CSV_LG)),
                 'PARTIAL_COL_TXT_SM': os.path.abspath(os.path.join(APP_DIR, PARTIAL_COL_TXT_SM)),
                 'PARTIAL_COL_CSV_SM': os.path.abspath(os.path.join(APP_DIR, PARTIAL_COL_CSV_SM)),
                 'PARTIAL_CSV_SM': os.path.abspath(os.path.join(APP_DIR, PARTIAL_CSV_SM)),
                 'FORECAST_PICKLE': os.path.abspath(os.path.join(APP_DIR, FORECAST_PICKLE)),
                 'RECOMMENDATION_PICKLE': os.path.abspath(os.path.join(APP_DIR, RECOMMENDATION_PICKLE)),
                 'PROFILE_PICKLE': os.path.abspath(os.path.join(APP_DIR, PROFILE_PICKLE)),
                 'COMPLETE_CSV_XSM': os.path.abspath(os.path.join(APP_DIR, COMPLETE_CSV_XSM)),}


def main():
    print(ABS_FILE_PATH)


if __name__ == '__main__':
    main()
