from random import random, uniform

from supplychainpy.demand.forecast_demand import Forecast


class Verbose:
    def __init__(self, parents: list = None, standard_error: float = None, smoothing_level: float = None):
        print('inside __init__')
        self.arg1 = parents
        self.arg2 = standard_error
        self.arg3 = smoothing_level

    def __call__(self, f):
        print('Inside __call__')

        def annotate(*args):
            for i in args:
                print('inside methods {}'.format(i))
            f(*args)

        return annotate()


class Individual:
    def __init__(self, name: str = 'offspring'):
        self._name = name
        self._genome = self.__genome_generator()

    def __repr__(self):
        return '{}: {}'.format(self._name, self._genome)

    @property
    def genome(self):
        return self._genome

    @property
    def name(self):
        return self._name

    @staticmethod
    def __genome_generator():
        genome = tuple([uniform(0, 1) for i in range(1, 12)])
        return genome


class Population:
    __slots__ = ['individuals']

    def __init__(self, individuals: list):
        self.individuals = individuals

    def reproduce(self):
        offsprings = []
        offspring = {}
        if len(self.individuals) > 1:
            for index, individual in enumerate(self.individuals):
                if index + 1 < len(self.individuals):
                    offspring = {key:value for key, value in individual.items() if value > 0}
                    offspring.update({key:value for key, value in individual.items() if value > 0})

            print(offspring)


    def _recombination(self):
        pass

    def _mutation(self):
        pass


class DiversifyPopulation(Population):
    def __init__(self, individuals: list):
        super().__init__(individuals)


class OptimiseSmoothingLevelGeneticAlgorithm:
    __generation = 0

    def __init__(self, orders: list, **kwargs):
        self.__orders = orders
        self.__average_order = kwargs['average_order']
        self.__population_size = kwargs['population_size']
        self.__standard_error = kwargs['standard_error']
        self.__smoothing_level = kwargs['smoothing_level']
        self.__initial_population = self.initialise_smoothing_level_evolutionary_algorithm_population()

    @property
    def initial_population(self):
        return self.__initial_population

    @property
    def population_size(self):
        return self.__population_size

    @population_size.setter
    def population_size(self, population_size):
        self.__population_size = population_size

    def initialise_smoothing_level_evolutionary_algorithm_population(self):
        """ Starts the process for creating the population. The number of parents is specified during the
         initialisation of the class. """

        parents = []
        parents_population=[]
        offspring = []
        population = []
        while len(parents_population) < self.__population_size:
            for i in range(0, self.__population_size):
                parent = Individual(name='parent')
                parents.append(parent)
            #print(parents)
                # generate offspring here to verify parents traits and allow most promising to produce offspring

            populations_genome = [i for i in self.generate_smoothing_level_genome(parents=parents,
                                                                                  standard_error=self.__standard_error,
                                                                                  smoothing_level=self.__smoothing_level)]

            populations_traits = [i for i in self.express_smoothing_level_genome(individuals_genome=populations_genome,
                                                                                 standard_error=self.__standard_error,
                                                                                 smoothing_level=self.__smoothing_level)]

            fit_population = self._population_fitness(population_xtraits=populations_traits)

            parents_population += fit_population

        #create_offspring = Population(individuals=parents_population)
        #create_offspring.reproduce()
        return parents_population

    @staticmethod
    def _population_fitness(population_xtraits: list) -> list:
        """ Assess the population for fitness before crossover and creating next generation. Positive traits
        should be reflected by more than 50% of the genome.

        Args:
            population_xtraits (list): A population with expressed traits. The standard_error representing the allele in the
            genome have been calculated and expressed as one or zero if below or above the orignal standard error respectively.

        Returns:
            fit_population (list):  A population of individuals with a probability of procreating above 50%.

        """
        fit_population = []
        for individual in population_xtraits:
            procreation_probability = sum(individual.values()) / len(individual.values())
            if procreation_probability >= 0.50:
                fit_population.append(individual)

        return fit_population

    def generate_smoothing_level_genome(self, parents: list, standard_error, smoothing_level):

        # stack parents and offspring into a list for next steps
        for parent in parents:
            individuals_genome = self._run_exponential_smoothing_forecast(parent.genome)
            #print(individuals_genome)
            # individuals_traits = self._express_trait(standard_error, smoothing_level, individuals_genome)

            yield individuals_genome

    def express_smoothing_level_genome(self, individuals_genome: list, standard_error, smoothing_level):

        # stack parents and offspring into a list for next steps
        for genome in individuals_genome:
            individuals_traits = self._express_trait(standard_error, smoothing_level, genome)
            yield individuals_traits

    def _run_exponential_smoothing_forecast(self, individual: tuple) -> dict:

        f = Forecast(self.__orders, self.__average_order)
        simple_expo_smoothing = []
        for sm_lvl in individual:
            p = [i for i in f.simple_exponential_smoothing(sm_lvl)]
            # print(p)
            simple_expo_smoothing.append(p)

        appraised_individual = {}
        for smoothing_level in individual:
            sum_squared_error = f.sum_squared_errors_indi(simple_expo_smoothing, smoothing_level)
            standard_error = f.standard_error(sum_squared_error, len(self.__orders), smoothing_level)
            appraised_individual.update({smoothing_level: standard_error})
        # print('The standard error as a trait has been calculated {}'.format(appraised_individual))
        return appraised_individual

    def _express_trait(self, original_standard_error: float, original_smoothing_level: float,
                       appraised_individual: dict):
        # fitness test? over 50% of the alleles must be positive traits. give percentage score
        # print(original_standard_error)
        for key in appraised_individual:
            if appraised_individual[key] < original_standard_error:
                appraised_individual[key] = 1
            else:
                appraised_individual[key] = 0
        # print('The traits have been verified {}'.format(appraised_individual))
        # check fitness of individual to procreate. 50% of traits need to be better smoothing_levels than the original
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

    evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=orders, average_order=avg_orders, smoothing_level=0.5,
                                                     population_size=10, standard_error=standard_error)
    # evo_mod.run_smoothing_level_evolutionary_algorithm(parents=evo_mod.initial_population,
    #                                                  standard_error=standard_error,
    #                                                  smoothing_level=0.5)
