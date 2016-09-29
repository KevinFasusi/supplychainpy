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
REL_PATH_GENETIC_ALGORITHM = '../sample_data/population_genome.txt'
REL_PATH_DASH = 'dash.pickle'
REL_PATH_ARCHIVE = '../../_archive/'
REL_PATH_CSV_MANAGEMENT_CONFIG = '../_pickled/csv_management_config.pickle'
REL_PATH_APPLICATION_CONFIG = '../_pickled/application_config.pickle'


ABS_FILE_PATH_DASH = os.path.abspath(os.path.join(APP_DIR, '../_pickled/', REL_PATH_DASH))
ABS_FILE_PATH_APPLICATION_CONFIG = os.path.abspath(os.path.join(APP_DIR, '../_pickled/', REL_PATH_APPLICATION_CONFIG))
ABS_FILE_PATH_CSV_MANAGEMENT_CONFIG = os.path.abspath(os.path.join(APP_DIR, REL_PATH_CSV_MANAGEMENT_CONFIG))
ABS_FILE_PATH_ARCHIVE = os.path.abspath(os.path.join(APP_DIR, REL_PATH_ARCHIVE))
ABS_FILE_GENETIC_ALGORITHM = os.path.abspath(os.path.join(APP_DIR, REL_PATH_ARCHIVE))

def main():
    print(ABS_FILE_PATH_APPLICATION_CONFIG)

if __name__ == '__main__':
    main()
