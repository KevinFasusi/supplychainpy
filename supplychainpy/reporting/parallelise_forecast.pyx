import concurrent
import logging
from concurrent.futures import ProcessPoolExecutor
from copy import deepcopy

from supplychainpy.inventory.analyse_uncertain_demand import UncertainDemand
log = logging.getLogger(__name__)
log.addHandler(logging.NullHandler())


def _analysis_forecast_simple(analysis: UncertainDemand) -> dict:
    """ Retrieves simple_exponentions_forecast from an instance of UncertainDemand.
        Function only required for Concurrent.futures.

    Args:
        analysis (UncertainDemand): Instance of UncertainDemand

    Returns:
        dict:   Forecast breakdown.
    """
    logging.log(logging.INFO,
                "Simple exponential smoothing forecast for SKU: {}\nObject id: {} ".format(
                    analysis.sku_id,
                    id(analysis)
                )
                )

    return analysis.simple_exponential_smoothing_forecast


def _analysis_forecast_holt(analysis: UncertainDemand) -> dict:
    """ Retrieves simple_exponentions_forecast from an instance of UncertainDemand.
        Function only required for Concurrent.futures.

    Args:
        analysis (UncertainDemand): Instance of UncertainDemand

    Returns:
        dict:   Forecast breakdown.
    """
    logging.log(logging.INFO,
                "Holt's trend corrected exponential smoothing forecast for SKU: {}\nObject id: {} ".format(
                    analysis.sku_id,
                    id(analysis)
                )
                )


    return analysis.holts_trend_corrected_forecast

def parallelise_ses(batched_analysis: list, core_count: int) -> dict:
    """ Execute the exponential smoothing forecaste in parallel.

    Args:
        batched_analysis: Uncertain demand objects batched for appropriate number of cores available on the host machine
        core_count: Number of cores available on the host machine, minus one.

    Returns:
        dict
    """
    simple_forecast = {}

    for unbatched in batched_analysis:
        with ProcessPoolExecutor(max_workers=core_count) as executor:
            simple_forecast_futures = {analysis.sku_id: executor.submit(_analysis_forecast_simple, analysis) for
                                       analysis in unbatched}
            simple_forecast_gen = {future: concurrent.futures.as_completed(simple_forecast_futures[future]) for
                                   future
                                   in simple_forecast_futures}
        try:
            simple_forecast.update( deepcopy(
                {value: simple_forecast_futures[value].result() for value in simple_forecast_gen}))
            del simple_forecast_futures
            del simple_forecast_gen
            executor.shutdown(wait=False)
        except OSError as err:
            print('{}'.format(err))
    return simple_forecast


def parallelise_htc(batched_analysis: list, core_count: int):
    """ Execute the Holts' trend corrected smoothing forecast in parallel.

    Args:
        batched_analysis: Uncertain demand objects batched for appropriate number of cores available on the host machine
        core_count: Number of cores available on the host machine, minus one.

    Returns:
        dict
    """
    holts_forecast = {}
    try:
        for unbatched in batched_analysis:
            with ProcessPoolExecutor(max_workers=core_count) as executor:
                holts_forecast_futures = {analysis.sku_id: executor.submit(_analysis_forecast_holt, analysis) for
                                          analysis
                                          in unbatched}
                holts_forecast_gen = {future: concurrent.futures.as_completed(holts_forecast_futures[future]) for future
                                      in
                                      holts_forecast_futures}
                holts_forecast.update(
                    {value: holts_forecast_futures[value].result() for value in holts_forecast_gen})
                executor.shutdown(wait=False)
    except TypeError as err:
        print('{}'.format(err))
    return holts_forecast