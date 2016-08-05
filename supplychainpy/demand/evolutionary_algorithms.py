from random import random, uniform

from supplychainpy.demand.forecast_demand import Forecast


class Individual:
    def __init__(self, name: str = 'offspring'):
        self._name = name
        self._genome = self.__genome_generator()

    @property
    def genome(self):
        return self._genome

    @property
    def name(self):
        return self._name

    @staticmethod
    def __genome_generator():
        genome = [uniform(0, 1) for i in range(1, 12)]
        return genome


class CreatePopulation:
    __slots__ = ['individuals']

    def __init__(self, individuals: list):
        self.individuals = individuals

    def Reproduce(self):
        if len(self.individuals) > 1:
            for individual in self.individuals:
                pass

    def _recombination(self):
        pass

    def _mutation(self):
        pass


class DiversifyPopulation(CreatePopulation):
    def __init__(self, individuals: list):
        super().__init__(individuals)


class ForecastingGeneticAlgorithms:
    def __init__(self, orders: list, average_order: float, smoothing_level: float):
        self.__orders = orders
        self.__average_order = average_order

    @staticmethod
    def initialise_smoothing_level_evolutionary_algorithm_population(number_of_parents):
        parents = []
        offspring = []

        def generate_population():
            for i in range(0, number_of_parents):
                parent = Individual(name='parent')
                parents.append(parent)
                # generate offspring here too
            return parents
        return generate_population()

    def run_smoothing_level_evolutionary_algorithm(self,parents:list, standard_error, smoothing_level):
        # stack parents and offspring into a list for next steps
        for parent in parents:
            appraised_individual = self._run_exponetial_smoothing_forecast(parent.genome)
            individuals_fitness = self._smoothing_level_fitness(standard_error, smoothing_level, appraised_individual)
            print(individuals_fitness)

    def _run_exponetial_smoothing_forecast(self, individual: list) -> dict:

        f = Forecast(self.__orders, self.__average_order)
        simple_expo_smoothing = []
        for sm_lvl in individual:
            simple_expo_smoothing.append(f.simple_exponential_smoothing(sm_lvl))

        appraised_individual = {}
        for smoothing_level in individual:
            sum_squared_error = f.sum_squared_errors(simple_expo_smoothing, smoothing_level)
            standard_error = f.standard_error(sum_squared_error, len(orders), smoothing_level)
            appraised_individual.update({smoothing_level: standard_error})
        print('The standard error as a trait has been calculated {}'.format(appraised_individual))
        return appraised_individual

    def _smoothing_level_fitness(self, original_standard_error: float, original_smoothing_level: float,
                                 appraised_individual: dict):
        # fitness test? over 50% of the alleles must be positive traits. give percentage score
        # print(original_standard_error)
        for key in appraised_individual:
            if appraised_individual[key] < original_standard_error:
                appraised_individual[key] = 1
            else:
                appraised_individual[key] = 0
        print('The trait has been tested for fitness {}'.format(appraised_individual))
        return appraised_individual

    def _selection_population(self, individuals_fitness: dict, appraised_individual: list):
        pass


if __name__ == '__main__':
    orders = [165, 171, 147, 143, 164, 160, 152, 150, 159, 169, 173, 203, 169, 166, 162, 147, 188, 161, 162, 169, 185,
              188, 200, 229, 189, 218, 185, 199, 210, 193, 211, 208, 216, 218, 264, 304]

    total_orders = 0
    avg_orders = 0
    for order in orders[:12]:
        total_orders += order

    avg_orders = total_orders / 12
    f = Forecast(orders, avg_orders)
    alpha = [0.2, 0.3, 0.4, 0.5, 0.6]
    s = [i for i in f.simple_exponential_smoothing(*alpha)]

    sum_squared_error = f.sum_squared_errors(s, 0.5)
    standard_error = f.standard_error(sum_squared_error, len(orders), 0.5)

    evo_mod = ForecastingGeneticAlgorithms(orders=orders, average_order=avg_orders, smoothing_level=0.5)
    evo_population = evo_mod.initialise_smoothing_level_evolutionary_algorithm_population(number_of_parents=10)
    evo_mod.run_smoothing_level_evolutionary_algorithm(parents=evo_population, standard_error=standard_error, smoothing_level=0.5)
