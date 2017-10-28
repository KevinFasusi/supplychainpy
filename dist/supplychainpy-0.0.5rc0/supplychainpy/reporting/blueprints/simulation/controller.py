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
import datetime

from flask import Flask

from supplychainpy._helpers._db_connection import database_connection_uri
from supplychainpy.reporting.blueprints.models import SimulationSummary, Simulation, MasterSkuList
from supplychainpy.reporting.config.settings import ProdConfig
from supplychainpy.reporting.extensions import db


def _retrieve_sku_id(db, sim):
    return db.session.query(MasterSkuList.id).filter(MasterSkuList.sku_id == sim.get('sku_id', 0)).first()


def select_last_simulation():
    app = Flask(__name__)
    app.config.from_object(ProdConfig)
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection_uri(retrieve='retrieve')
    with app.app_context():
        simulation_sub = db.session.query(db.func.max(Simulation.date))
        simulation_id = db.session.query(Simulation).filter(Simulation.date == simulation_sub).first()
        return db.session.query(SimulationSummary).filter(SimulationSummary.sim_id == simulation_id.id).all()

def store_simulation(sim_summary: dict):
    app = Flask(__name__)
    app.config.from_object(ProdConfig)
    db.init_app(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = database_connection_uri(retrieve='retrieve')
    with app.app_context():
        simulation = Simulation()
        simulation.date = datetime.datetime.now()
        db.session.add(simulation)
        db.session.commit()
        simulation_sub = db.session.query(db.func.max(Simulation.date))
        simulation_id = db.session.query(Simulation).filter(Simulation.date == simulation_sub).first()
        for sim in sim_summary:
            master_sku_id = _retrieve_sku_id(db, sim)
            simulation_summary = SimulationSummary()
            simulation_summary.sku_id = master_sku_id.id
            simulation_summary.sim_id = simulation_id.id
            simulation_summary.average_backlog = sim.get('average_backlog', 0)
            simulation_summary.variance_opening_stock = sim.get('variance_opening_stock', 0)
            simulation_summary.minimum_opening_stock = sim.get('minimum_opening_stock', 0)
            simulation_summary.maximum_closing_stock = sim.get('maximum_closing_stock', 0)
            simulation_summary.maximum_quantity_sold = sim.get('maximum_quantity_sold', 0)
            simulation_summary.maximum_backlog = sim.get('maximum_backlog', 0)
            simulation_summary.average_backlog = sim.get('average_backlog', 0)
            simulation_summary.minimum_closing_stock = sim.get('minimum_closing_stock', 0)
            simulation_summary.minimum_backlog = sim.get('minimum_backlog', 0)
            simulation_summary.minimum_quantity_sold = sim.get('minimum_quantity_sold', 0)
            simulation_summary.average_quantity_sold = sim.get('average_quantity_sold', 0)
            simulation_summary.maximum_opening_stock = sim.get('maximum_opening_stock', 0)
            simulation_summary.standard_deviation_quantity_sold = sim.get('standard_deviation_quantity_sold', 0)
            simulation_summary.standard_deviation_closing_stock = sim.get('standard_deviation_closing_stock', 0)
            simulation_summary.average_closing_stock = sim.get('average_closing_stock', 0)
            simulation_summary.standard_deviation_backlog = sim.get('standard_deviation_backlog', 0)
            simulation_summary.average_shortage_units = sim.get('average_shortage_units', 0)
            db.session.add(simulation_summary)
            db.session.commit()
