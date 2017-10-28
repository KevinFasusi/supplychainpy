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


from supplychainpy.reporting.extensions import db


def convert_datetime(value):
    """Deserialize datetime object into string"""
    if value is None:
        return None
    return [value.strftime("%d-%m-%y"), value.strftime("%H:%M:%S")]


class MasterSkuList(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    sku_id = db.Column(db.String(255))
    analysis = db.relationship("InventoryAnalysis", backref='sku', lazy='dynamic')
    simulation_summary_id = db.relationship("SimulationSummary", backref='sim', lazy='dynamic')


class Currency(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    fx = db.relationship("InventoryAnalysis", backref='currency', lazy='dynamic')
    currency_code = db.Column(db.String(3))
    country = db.Column(db.String(255))
    symbol = db.Column(db.String(255))


class TransactionLog(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    transaction = db.relationship("InventoryAnalysis", backref='log', lazy='dynamic')
    profile_recommendation = db.relationship("ProfileRecommendation", backref='profile', lazy='dynamic')


class InventoryAnalysis(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    sku_id = db.Column(db.Integer, db.ForeignKey('master_sku_list.id'))
    abc_xyz_classification = db.Column(db.String(2))
    standard_deviation = db.Column(db.Integer())
    safety_stock = db.Column(db.Integer())
    reorder_level = db.Column(db.Integer())
    economic_order_quantity = db.Column(db.Integer())
    demand_variability = db.Column(db.Integer())
    average_orders = db.Column(db.Float())
    shortages = db.Column(db.Integer())
    excess_stock = db.Column(db.Integer())
    reorder_quantity = db.Column(db.Integer())
    economic_order_variable_cost = db.Column(db.Float())
    unit_cost = db.Column(db.Numeric(12, 2))
    revenue = db.Column(db.Float())
    date = db.Column(db.DateTime())
    safety_stock_rank = db.Column(db.Integer())
    shortage_rank = db.Column(db.Integer())
    excess_cost = db.Column(db.Numeric(12, 2))
    percentage_contribution_revenue = db.Column(db.Float)
    excess_rank = db.Column(db.Integer())
    retail_price = db.Column(db.Numeric(18, 2))
    gross_profit_margin = db.Column(db.Numeric(12, 2))
    min_order = db.Column(db.Integer())
    safety_stock_cost = db.Column(db.Numeric(18, 2))
    revenue_rank = db.Column(db.Integer())
    markup_percentage = db.Column(db.Float())
    max_order = db.Column(db.Integer())
    shortage_cost = db.Column(db.Numeric(18, 2))
    quantity_on_hand = db.Column(db.Integer())
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'))
    transaction_log_id = db.Column(db.Integer, db.ForeignKey('transaction_log.id'))
    orders_id = db.relationship("Orders", backref='demand', lazy='dynamic')
    forecast_id = db.relationship("Forecast", backref='forecasts', lazy='dynamic')
    forecast_breakdown_id = db.relationship("ForecastBreakdown", backref='estimates', lazy='dynamic')
    inventory_turns = db.Column(db.Float())
    traffic_light = db.Column(db.String(6))
    recommendation_id = db.relationship("Recommendations", backref='rec', lazy='dynamic')
    backlog = db.Column(db.Integer())

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.sku_id,
            'revenue': self.revenue,
            'classification': self.abc_xyz_classification,
            'eoq': self.economic_order_quantity,
            'Date': convert_datetime(self.date),
            'standard_deviation': self.standard_deviation,
            'safety_stock': self.safety_stock,
            'reorder_level': self.reorder_level,
            'economic_order_quantity': self.economic_order_quantity,
            'demand_variability': self.demand_variability,
            'average_orders': round(self.average_orders),
            'shortages': self.shortages,
            'excess_stock': self.excess_stock,
            'reorder_quantity': float(self.reorder_quantity),
            'economic_order_variable_cost': float(self.economic_order_variable_cost),
            'unit_cost': float(self.unit_cost),
            'safety_stock_rank': self.safety_stock_rank,
            'shortage_rank': self.shortage_rank,
            'excess_cost': float(self.excess_cost),
            'percentage_contribution_revenue': float(self.percentage_contribution_revenue),
            'excess_rank': self.excess_rank,
            'retail_price': float(self.retail_price),
            'gross_profit_margin': float(self.gross_profit_margin),
            'min_order': self.min_order,
            'safety_stock_cost': float(self.safety_stock_cost),
            'revenue_rank': self.revenue_rank,
            'markup_percentage': self.markup_percentage,
            'max_order': self.max_order,
            'shortage_cost': float(self.shortage_cost),
            'quantity_on_hand': self.quantity_on_hand,
            'inventory_turns': self.inventory_turns
        }


class Orders(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    order_quantity = db.Column(db.Integer())
    rank = db.Column(db.Integer())


class ForecastType(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    type = db.Column(db.String(10))
    forecast_id = db.relationship("Forecast", backref='type', lazy='dynamic')
    forecast_statistic_id = db.relationship("ForecastStatistics", backref='details', lazy='dynamic')
    forecast_breakdown_id = db.relationship("ForecastBreakdown", backref='breakdown', lazy='dynamic')


class Forecast(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    forecast_quantity = db.Column(db.Integer())
    forecast_type_id = db.Column(db.Integer, db.ForeignKey('forecast_type.id'))
    period = db.Column(db.Integer())
    create_date = db.Column(db.DateTime())


class ForecastStatistics(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    forecast_type_id = db.Column(db.Integer, db.ForeignKey('forecast_type.id'))
    slope = db.Column(db.Float())
    p_value = db.Column(db.Float())
    test_statistic = db.Column(db.Float())
    slope_standard_error = db.Column(db.Float())
    intercept = db.Column(db.Float())
    standard_residuals = db.Column(db.Float())
    trending = db.Column(db.Boolean)
    mape = db.Column(db.Float())
    optimal_alpha = db.Column(db.Float())
    optimal_gamma = db.Column(db.Float())


class ForecastBreakdown(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    period = db.Column(db.Integer())
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    forecast_type_id = db.Column(db.Integer, db.ForeignKey('forecast_type.id'))
    level_estimates = db.Column(db.Float())
    trend = db.Column(db.Float())
    one_step_forecast = db.Column(db.Float())
    forecast_error = db.Column(db.Float())
    squared_error = db.Column(db.Float())
    regression = db.Column(db.Float())


class Recommendations(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    analysis_id = db.Column(db.Integer, db.ForeignKey('inventory_analysis.id'))
    statement = db.Column(db.Text())


class ProfileRecommendation(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transaction_log.id'))
    statement = db.Column(db.Text())


class Simulation(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime())
    runs = db.Column(db.Integer())
    sim_summary_id = db.relationship("SimulationSummary", backref='simulation', lazy='dynamic')


class SimulationSummary(db.Model):
    __table_args__ = {'sqlite_autoincrement': True}
    id = db.Column(db.Integer(), primary_key=True)
    sku_id = db.Column(db.Integer, db.ForeignKey('master_sku_list.id'))
    sim_id = db.Column(db.Integer, db.ForeignKey('simulation.id'))
    variance_opening_stock = db.Column(db.Integer())
    minimum_opening_stock = db.Column(db.Integer())
    maximum_closing_stock =  db.Column(db.Integer())
    maximum_quantity_sold = db.Column(db.Integer())
    maximum_backlog = db.Column(db.Integer())
    average_backlog = db.Column(db.Integer())
    minimum_closing_stock = db.Column(db.Integer())
    minimum_backlog = db.Column(db.Integer())
    minimum_quantity_sold = db.Column(db.Integer())
    average_quantity_sold = db.Column(db.Integer())
    maximum_opening_stock = db.Column(db.Integer())
    standard_deviation_quantity_sold = db.Column(db.Integer())
    standard_deviation_closing_stock = db.Column(db.Integer())
    average_closing_stock = db.Column(db.Integer())
    standard_deviation_backlog = db.Column(db.Integer())
    average_shortage_units = db.Column(db.Integer())
