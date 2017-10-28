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
from _decimal import Decimal
from concurrent.futures import ThreadPoolExecutor

import flask
from flask import Blueprint, request, abort

from supplychainpy import simulate
from supplychainpy._helpers._config_file_paths import ABS_FILE_PATH_APPLICATION_CONFIG
from supplychainpy._helpers._enum_formats import FileFormats
from supplychainpy._helpers._pickle_config import deserialise_config
from supplychainpy.model_inventory import analyse
from supplychainpy.reporting.blueprints.models import MasterSkuList
from supplychainpy.reporting.blueprints.simulation.controller import store_simulation, select_last_simulation
from supplychainpy.reporting.extensions import db

simulation_blueprint = Blueprint('simulation', __name__, template_folder='templates')


def page_not_found(e):
    print('hello')
    return flask.render_template('404.html'), 404


def run_simulation():
    pass
    

@simulation_blueprint.route('/simulation', methods=['GET','PUT'])
@simulation_blueprint.route('/simulation/<int:runs>', methods=['GET','PUT'])
def simulation(runs:int=None):
    try:
        database_path = ''
        file_name = ''
        sim_results = []
        sim_summary_results = []
        inventory = []

        if runs is not None:
            config = deserialise_config(ABS_FILE_PATH_APPLICATION_CONFIG)
            database_path = config['database_path']
            file_name = config['file']
            file_path = database_path.replace(' ','') + '/' +(file_name.replace(' ',''))
            analysed_orders = analyse(file_path=str(file_path), z_value=Decimal(1.28), reorder_cost=Decimal(5000), file_type=FileFormats.csv.name, length=12, currency='USD')
            # run the simulation, populate a database and then retrieve the most current values for the simulation page.
            try:
                with ThreadPoolExecutor(max_workers=1) as executor:
                    sim = executor.submit(simulate.run_monte_carlo, orders_analysis=analysed_orders, runs=runs, period_length=12)
                    sim_results = sim.result()
                    sim_window = executor.submit(simulate.summarize_window, simulation_frame=sim_results, period_length=12)
                    sim_window_result = sim_window.result()
                    sim_summary = executor.submit(simulate.summarise_frame, sim_window_result)
                    sim_summary_results = sim_summary.result()
                    store_simulation(sim_summary_results)
                inventory = db.session.query(MasterSkuList).all()

            except OSError as e:
                print(e)
        elif runs is None and request.method == 'GET':
            try:
                sim_summary_results = select_last_simulation()
                inventory = db.session.query(MasterSkuList).all()
            except AttributeError as e:
                pass

        return flask.render_template('simulation.html', db= database_path, file_name=file_name, sim=sim_summary_results, runs=sim_results, inventory=inventory)
    except OSError:
        abort(404)

if __name__ == '__main__':
    simulation()