def _forecast_error(demand: int, one_step_forecast: float):
        return float(demand) - one_step_forecast


def holts_trend_corrected_exponential_smoothing(self, alpha: float, gamma: float, intercept: float, slope: float):
        forecast = {}
        #log.debug('holts ')
        current_level_estimate = intercept
        forecast.update({'alpha': alpha,
                         'gamma': gamma,
                         't': 0,
                         'demand': 0,
                         'level_estimates': current_level_estimate,
                         'trend': slope,
                         'one_step_forecast': 0,
                         'forecast_error': 0,
                         'squared_error': 0

                         })
        previous_trend = slope
        previous_level_estimate = current_level_estimate
        for index, demand in enumerate(tuple(self.__orders), 1):
            #log.debug('demand: {}'.format(demand))
            one_step = previous_level_estimate + previous_trend
            #log.debug('one_step: {}'.format(one_step))
            forecast_error = _forecast_error(demand, one_step)
            #log.debug('forecast_error: {}'.format(forecast_error))
            current_trend = self._holts_trend(previous_trend, gamma, alpha, forecast_error)
            #log.debug('trend: {}'.format(current_trend))
            current_level_estimate = self._level_estimate_holts_trend_corrected(previous_level_estimate,
                                                                                alpha,
                                                                                previous_trend,
                                                                                forecast_error)
            #log.debug('current_level: {}'.format(current_level_estimate))
            squared_error = forecast_error ** 2
            yield {'alpha': alpha,
                   'gamma': gamma,
                   't': index,
                   'demand': demand,
                   'trend': current_trend,
                   'level_estimates': current_level_estimate,
                   'one_step_forecast': one_step,
                   'forecast_error': forecast_error,
                   'squared_error': squared_error
                   }
            #log.debug('squared_error: {}'.format(squared_error))
            previous_level_estimate = current_level_estimate
            previous_trend = current_trend