from random import uniform

from supplychainpy.demand._forecast_demand import Forecast
from supplychainpy.demand.regression import LinearRegression

class Individual:
    _genome = 0

    def __init__(
            self, name ='offspring', overide=False, int gene_count =12,
            forecast_type ='ses'
        ):

        self._name = name
        self._gene_count = gene_count
        self._forecast_type = forecast_type
        if not overide:
            self._genome = self.__genome_generator()

    def __repr__(self):
        return '{}: {}'.format(self._name, self._genome)

    @property
    def gene_count(self):
        return self.gene_count

    @gene_count.setter
    def gene_count(self, int value):
        self._gene_count = value

    @property
    def genome(self):
        return self._genome

    @genome.setter
    def genome(self, tuple val):
        self._genome = val

    @property
    def name(self):
        return self._name

    def __genome_generator(self):
        genome = ()
        if self._forecast_type == 'ses':
            genome = ([uniform(0, 1) for i in range(0, self._gene_count)])
        else:
            genome = ([(uniform(0, 1), uniform(0, 1)) for i in range(0, self._gene_count)])

        return genome


class Population:
    """ Create a population of individuals to reproduce. """

    __slots__ = ['individuals', 'mutation_probability']
    _recombination_type = ('single_point', 'two_point', 'uniform')

    def __init__(self, list individuals, double mutation_probability = 0.2):
        self.individuals = individuals
        self.mutation_probability = mutation_probability
        #print("initialising {}".format(id(self)))

    def reproduce(self, recombination_type = 'single_point'):
        """ Coordinates the reproduction of two individuals, using one of three recombination methods 'single_point,
        two_point or uniform'.

        Args:
            recombination_type: The method of recombination used to

        Yields:
            (dict):     The result of recombination and mutation.

        """
        

        if recombination_type == self._recombination_type[0]:
      
            yield [i for i in self._single_point_crossover_recombination()][0]
        if recombination_type == self._recombination_type[1]:
            yield [i for i in self._two_point_crossover_recombination()][0]
        if recombination_type == self._recombination_type[2]:
            yield [i for i in self._uniform_crossover_recombination()][0]

    def _single_point_crossover_recombination(self):
        """ Selects genes from the parent to crossover based on one point along the chromosome.

        Yields:
            individual (dict):          Parents p1-xxxxxxxxxxxx and p2-oooooooooooo will produce offspring c1-xxxxxxooooo
                                        and c2-ooooooxxxxxx. Individual yields the first offspring (c1).
            individual_two (dict):      Parents p1-xxxxxxxxxxxxx and p2-oooooooooooo will produce offspring c1-xxxxxxooooo
                                        and c2-ooooooxxxxxx. Individual_two yields the second offspring (c2).
        """

        cdef int genome_count = 0
        cdef dict new_individual = {}
        cdef dict new_individual_two = {}

        cdef int mutation_count = 0
        cdef int mutation_index = 0

        try:

            if len(self.individuals) > 1:
                for index, individual in enumerate(self.individuals):
                    for key, value in individual.items():
                        population_allele_count = len(self.individuals) * len(individual.items())
                        number_of_mutations_allowed = round(population_allele_count * self.mutation_probability)
                        mutation_index += 1
                        if (genome_count <= 5 and len(new_individual) < 12) or (
                                            18 >= genome_count > 12 > len(new_individual)):

                            if mutation_index == number_of_mutations_allowed:
                                new_individual.update(self._mutation({key: value}))
                                genome_count += 1
                                mutation_index = 0
                                mutation_count += 1
                            else:
                                new_individual.update({key: value})
                                genome_count += 1

                        elif (genome_count >= 6 and len(new_individual_two) < 12) or (18 < genome_count <= 24 and len(
                                new_individual) < 12):

                            if mutation_index == number_of_mutations_allowed:
                                new_individual_two.update(self._mutation({key: value}))
                                genome_count += 1
                                mutation_index = 0
                                mutation_count += 1
                            else:
                                new_individual.update({key: value})
                                genome_count += 1

                        else:
                            genome_count += 1

                        if genome_count == 24:
                            genome_count = 0
                            # if new_individual != new_individual_two:
                            # log.debug('single point crossover was successful')
                            # else:
                            # log.debug('single point crossover resulted in clone of parent')
                            yield (new_individual)
                            yield (new_individual_two)

            else:
                raise ValueError()

        except ValueError:
            print('Population Size is too small for effective genetic recombination and reproduction of offspring')

    def _two_point_crossover_recombination(self):
        """ Selects genes from the parent to crossover based on two points along the chromosome.

        Yields:
            individual (dict):          Parents p1-xxxxxxxxxxxxx and p2-oooooooooooo will produce offspring c1-xxxooooooxxx
                                        and c2-oooxxxxxxooo. Individual yields the first offspring (c1).
            individual_two (dict):      Parents p1-xxxxxxxxxxxxx and p2-oooooooooooo will produce offspring c1-xxxooooooxxx
                                        and c2-oooxxxxxxooo. Individual_two yields the second offspring (c2).
        """

        cdef int genome_count = 0
        cdef dict new_individual = {}

        cdef int mutation_count = 0
        cdef int mutation_index = 0
        cdef dict new_individual_two = {}

        try:
            if len(self.individuals) > 1:
                for index, individual in enumerate(self.individuals):
                    for key, value in individual.items():
                        population_allele_count = len(self.individuals) * len(individual.items())
                        number_of_mutations_allowed = round(population_allele_count * self.mutation_probability)
                        mutation_index += 1
                        if (2 >= genome_count and len(new_individual) < 12) or (15 <= genome_count <= 20) or (
                                        9 <= genome_count <= 11):
                            if mutation_index == number_of_mutations_allowed:
                                new_individual.update(self._mutation({key: value}))
                                genome_count += 1
                                mutation_index = 0
                                mutation_count += 1
                            else:
                                new_individual.update({key: value})
                                genome_count += 1

                        elif (12 <= genome_count <= 14 and len(new_individual_two) < 12) or (
                                        3 <= genome_count <= 8) and (len(
                            new_individual) < 12 or 21 <= genome_count <= 23):
                            if mutation_index == number_of_mutations_allowed:
                                new_individual.update(self._mutation({key: value}))
                                genome_count += 1
                                mutation_index = 0
                                mutation_count += 1
                            else:
                                new_individual.update({key: value})
                                genome_count += 1
                        else:
                            genome_count += 1

                        if genome_count == 24:
                            genome_count = 0
                            # if new_individual != new_individual_two:
                            # log.debug('single point crossover was successful')
                            # else:
                            # log.debug('single point crossover resulted in clone of parent')
                            yield (new_individual)
                            yield (new_individual_two)



        except OSError as e:

            print(e)

    # TODO-feature uniform crossover recombination for reproduction
    def _uniform_crossover_recombination(self):
        pass

    @staticmethod
    def _mutation(gene: dict):
        """Mutates a gene and reinserts it into the chromosome. A phenotype expressed as a standard error is altered
        by having the bit representing it flipped.

        Args:
            gene:   The alpha value and bit representing the positive or negative fit of the gene.

        Returns:
            dict:   The new gene with an altered value for the it representing the positive or negative fit of the gene.

        """

        original_gene = [[k, v] for k, v in gene.items()]

        def mutate():

            if original_gene[0][1] == 0:
                return {original_gene[0][0]: 1}
            elif original_gene[0][1] == 1:
                return {original_gene[0][0]: 0}
            else:
                return {original_gene[0][0]: original_gene[0][0]}

        return mutate()



class OptimiseSmoothingLevelGeneticAlgorithm:
    __generation = 0

    def __init__(self, orders: list, **kwargs):
        self.__orders = orders
        if len(kwargs) != 0:
            self.__average_order = kwargs['average_order']
            self.__population_size = kwargs['population_size']
            self.__standard_error = kwargs['standard_error']
            self.__recombination_type = kwargs['recombination_type']

    def initial_population(self, individual_type = 'ses'):
        """Initialises population and initiates the optimisation of the standard error by searching for an optimum
        alpha value.
        Returns:

        """
        return self._initialise_smoothing_level_evolutionary_algorithm_population(individual_type=individual_type)

    @property
    def population_size(self):
        return self.__population_size

    @population_size.setter
    def population_size(self, population_size):
        self.__population_size = population_size

    def _initialise_smoothing_level_evolutionary_algorithm_population(self, individual_type: str):
        """ Starts the process for creating the population. The number of parents is specified during the
         initialisation of the class. """

        cdef list parents = []
        cdef list parents_population = []
        cdef list populations_genome = []
        cdef list populations_traits = []

        while len(parents_population) < self.__population_size:
            for i in range(0, self.__population_size):
                parent = Individual(name='parent', forecast_type=individual_type)
                parents.append(parent)

            populations_genome = [i for i in self.generate_smoothing_level_genome(population=parents,
                                                                                  individual_type=individual_type)]
            populations_traits = [i for i in self.express_smoothing_level_genome(individuals_genome=populations_genome,
                                                                                 standard_error=self.__standard_error)]

            fit_population = [i for i in
                              self._population_fitness(population=populations_traits, individual_type=individual_type)]


            parents_population += fit_population

        create_offspring = Population(individuals=parents_population)

        cdef list new_population = []
        # population reproduce
        new_population = [i for i in create_offspring.reproduce(recombination_type=self.__recombination_type)]

        if new_population is None:
            return 0

        cdef list parent_offspring_population = []
        cdef list new_individuals = []
        cdef list new_populations_traits = []
        cdef list new_fit_population = []
        cdef list final_error = []
        cdef tuple minimum_smoothing_level

        while len(new_population) < self.__population_size * 10:
            for po in new_population:
                pke = po.keys()
                parent_offspring_population.append(tuple(pke))

            for genome in parent_offspring_population:
                new_individual = Individual(overide=True)
                new_individual.genome = genome
                new_individuals.append(new_individual)

            # while population allele boundary ie 50 70 95 is less than specified number.
            new_population_genome = [i for i in self.generate_smoothing_level_genome(population=new_individuals,
                                                                                     individual_type=individual_type)]

            new_populations_traits = [i for i in
                                      self.express_smoothing_level_genome(individuals_genome=new_population_genome,
                                                                          standard_error=self.__standard_error)]

            new_fit_population = [i for i in self._population_fitness(population=new_populations_traits,
                                                                      individual_type=individual_type)]
            new_population = new_fit_population

        new_individuals.clear()

        new_individuals = [i for i in self.create_individuals(new_population)]

        final_error = [i for i in self.generate_smoothing_level_genome(population=new_individuals,
                                                                       individual_type=individual_type)]

        minimum_smoothing_level = min(zip(final_error[0].values(), final_error[0].keys()))

        return minimum_smoothing_level

    @staticmethod
    def create_individuals(list new_population):
        """Create individuals using class from genomes striped during processing fitness.
        Args:
            new_population (list):  new population of individual genomes.
        """
        cdef list parent_offspring_population = []

        for po in new_population:
            pke = po.keys()
            parent_offspring_population.append(tuple(pke))

        for genome in parent_offspring_population:
            new_individual = Individual(overide=True)
            new_individual.genome = genome
            yield new_individual

    @staticmethod
    def _population_fitness(list population, individual_type='ses'):
        """ Assess the population for fitness before crossover and creating next generation. Positive traits
        should be reflected by more than 70% of the genes in the genome.

        Args:
            population (list): A population with expressed traits (phenotypes). The standard_errors representing
            the genome of the individual have been calculated and expressed as one or zero if below or above
            the original standard error respectively.

        Returns:
            fit_population (list):  A population of individuals with a probability of procreating above 70% for simple
                                    exponential smoothing and 30% for holts trend correcting. """
        cdef double procreation_probability
        for individual in population:
            procreation_probability = sum(individual.values()) / len(individual.values())
            if individual_type == 'ses':
                if procreation_probability >= 0.4:
                    yield individual
            else:
                if procreation_probability >= 0.3:
                    yield individual

    def generate_smoothing_level_genome(self, list population, individual_type = 'ses'):

        # stack parents and offspring into a list for next steps
        if individual_type == 'ses':
            for parent in population:
                individuals_genome = self._run_exponential_smoothing_forecast(parent.genome)
                # print(individuals_genome)
                # individuals_traits = self._express_trait(standard_error, smoothing_level, individuals_genome)

                yield individuals_genome
        else:
            for parent in population:
                individuals_genome = self._run_holts_trend_corrected_exponential_smoothing(parent.genome)
                # print(individuals_genome)
                # individuals_traits = self._express_trait(standard_error, smoothing_level, individuals_genome)

                yield individuals_genome

    @staticmethod
    def htce_para(forecast, alpha, gamma, intercept, slope):
        return [i for i in forecast.holts_trend_corrected_exponential_smoothing(alpha=alpha, gamma=gamma,
                                                                                intercept=intercept,
                                                                                slope=slope)]


    def sum_squared_error_para(self, forecast, holts_trend_corrected_smoothing, alpha, gamma, smoothing_level):
        appraised_individual = {}
        sum_squared_error = forecast.sum_squared_errors_indi_htces(squared_error=holts_trend_corrected_smoothing,
                                                            alpha=alpha, gamma=gamma)
        standard_error = forecast.standard_error(sum_squared_error, len(self.__orders), smoothing_level)
        appraised_individual.update({smoothing_level: standard_error})
        return appraised_individual

    def _run_holts_trend_corrected_exponential_smoothing(self, individual: tuple):
        f = Forecast(self.__orders, self.__average_order)
        holts_trend_corrected_smoothing = []
        demand = [{'t': index, 'demand': order} for index, order in enumerate(self.__orders, 1)]
        stats = LinearRegression(demand)
        log_stats = stats.least_squared_error(slice_end=6)

        for sm_lvl in individual:
            p = [i for i in f.holts_trend_corrected_exponential_smoothing(alpha=sm_lvl[0], gamma=sm_lvl[1],
                                                                          intercept=log_stats.get('intercept'),
                                                                          slope=log_stats.get('slope'))]
            # print(p)
            holts_trend_corrected_smoothing.append(p)

        appraised_individual = {}
        for smoothing_level in individual:
            sum_squared_error = f.sum_squared_errors_indi_htces(squared_error=holts_trend_corrected_smoothing,
                                                                alpha=smoothing_level[0], gamma=smoothing_level[1])
            standard_error = f.standard_error(sum_squared_error, len(self.__orders), smoothing_level)
            appraised_individual.update({smoothing_level: standard_error})
        # print('The standard error as a trait has been calculated {}'.format(appraised_individual))
        return appraised_individual

    def express_smoothing_level_genome(self, individuals_genome: list, standard_error):

        # stack parents and offspring into a list for next steps
        for genome in individuals_genome:
            individuals_traits = self._express_trait(standard_error, genome)
            yield individuals_traits

    def _run_exponential_smoothing_forecast(self, individual ):

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

    @staticmethod
    def _express_trait(original_standard_error: float, appraised_individual: dict):
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

    def simple_exponential_smoothing_evo(self, smoothing_level_constant, initial_estimate_period,
                                         recombination_type = 'single_point', int population_size = 10,
                                         int forecast_length = 5):
        """ Simple exponential smoothing using evolutionary algorithm for optimising smoothing level constant (alpha value)

            Args:
                initial_estimate_period (int):      The number of previous data points required for initial level estimate.
                smoothing_level_constant (float):   Best guess at smoothing level constant appropriate for forecast.

           Returns:
               dict:

            Example:

        """
        if None != self.__recombination_type:
            recombination_type = self.__recombination_type

        sum_orders = 0

        for demand in self.__orders[:initial_estimate_period]:
            sum_orders += demand

        avg_orders = sum_orders / initial_estimate_period

        forecast_demand = Forecast(self.__orders, avg_orders)

        ses_forecast = [i for i in forecast_demand.simple_exponential_smoothing(*(smoothing_level_constant,))]

        sum_squared_error = forecast_demand.sum_squared_errors(ses_forecast, smoothing_level_constant)

        standard_error = forecast_demand.standard_error(sum_squared_error, len(self.__orders),
                                                        smoothing_level_constant)

        evo_mod = OptimiseSmoothingLevelGeneticAlgorithm(orders=self.__orders,
                                                         average_order=avg_orders,
                                                         smoothing_level=smoothing_level_constant,
                                                         population_size=population_size,
                                                         standard_error=standard_error,
                                                         recombination_type=recombination_type)

        optimal_alpha = evo_mod.initial_population()

        optimal_ses_forecast = [i for i in forecast_demand.simple_exponential_smoothing(optimal_alpha[1])]

        ape = LinearRegression(optimal_ses_forecast)
        mape = forecast_demand.mean_aboslute_percentage_error_opt(optimal_ses_forecast)
        stats = ape.least_squared_error()
        simple_forecast = forecast_demand.simple_exponential_smoothing_forecast(forecast=optimal_ses_forecast,
                                                                                forecast_length=forecast_length)
        regression = {
            'regression': [(stats.get('slope') * i) + stats.get('intercept') for i in range(0, 12)]}
        return {'forecast_breakdown': optimal_ses_forecast, 'mape': mape, 'statistics': stats,
                'forecast': simple_forecast, 'optimal_alpha': optimal_alpha[1], 'standard_error': standard_error,
                'regression': [i for i in regression.get('regression')]}
