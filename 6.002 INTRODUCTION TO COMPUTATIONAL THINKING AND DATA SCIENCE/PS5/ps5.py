# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: Berkay Yaldız
# Collaborators (discussion):
# Time:

from audioop import mul
from cProfile import label
from cv2 import line
import pylab
import re

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""


class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """

    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)',
                            items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature

        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]


def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]


"""
End helper code
"""


def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    coef_arrays = []
    for deg in degs:
        coef_arrays.append(
            pylab.polyfit(x, y, deg))
    return coef_arrays


def r_squared(y, estimated):
    """
    Calculate the R-squared error term.

    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    return 1-(pylab.sum(pylab.square(y-estimated)) / pylab.sum(pylab.square(y-y.mean())))


def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        power_array = pylab.array(list(range(len(model)-1, 0, -1)))
        estimated_values = pylab.zeros(len(x))
        index = 0
        for x_value in x:
            estimated_values[index] = pylab.sum(
                model[:-1] * (pylab.float64(x_value) ** power_array)) + model[-1]
            index += 1
        pylab.figure()
        pylab.plot(x, y, 'o', label='original')
        pylab.plot(x, estimated_values, '-r', label='estimated')
        pylab.legend()
        pylab.xlabel("Years")
        pylab.ylabel("Celcius Degrees")
        r_square_value = r_squared(y, estimated_values)
        title_string = "Celcius Degree vs Years \n $R^2$ = " + \
            str(r_square_value) + "\n" + \
            "Degree of the model = " + str(len(model)-1)
        if len(model) == 2:
            se_over_slope_value = se_over_slope(x, y, estimated_values, model)
            title_string += "\n Ratio of the standard error of fitted curve's slope to slope = " + \
                str(se_over_slope_value)
        pylab.title(title_string)
        pylab.grid()
        pylab.show()


def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    average_temp = pylab.zeros(len(years))
    index1 = 0
    for index in years:
        summer = 0
        data_length = 0
        for city in multi_cities:
            temp_data = climate.get_yearly_temp(
                city, index)  # Hold the returned data
            # Sum every temperature in that year and city.
            summer += pylab.sum(temp_data)
            # Increase as the length of the temperature data.
            data_length += len(temp_data)
        average_temp[index1] = summer / data_length
        index1 += 1
    return average_temp


def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    length_of_array = len(y)
    averaged_array = pylab.zeros(length_of_array)
    for index in range(window_length):
        averaged_array[index] = pylab.sum(y[:index+1]) / (index+1)
    for index in range(window_length, length_of_array):
        averaged_array[index] = pylab.sum(
            y[index-window_length+1:index+1]) / window_length
    return averaged_array


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    return pylab.sqrt(pylab.mean((y-estimated)**2))


def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual
        city temperatures for the given cities in a given year.
    """
    std_deviation_temp = pylab.zeros(len(years))
    averaged_temp = gen_cities_avg(climate, multi_cities, years)
    index1 = 0
    for index in years:
        temp_data = 0
        for city in multi_cities:
            temp_data += climate.get_yearly_temp(
                city, index)  # Hold the returned data
        temp_data /= len(multi_cities)
        std_deviation_temp[index1] = pylab.sqrt(
            pylab.mean((temp_data - averaged_temp[index1]) ** 2))
        index1 += 1
    return std_deviation_temp


def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points.

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    for model in models:
        power_array = pylab.array(list(range(len(model)-1, 0, -1)))
        estimated_values = pylab.zeros(len(x))
        index = 0
        for x_value in x:
            estimated_values[index] = pylab.sum(
                model[:-1] * (pylab.float64(x_value) ** power_array)) + model[-1]  # Overflow, so make it float.
            index += 1
        pylab.figure()
        pylab.plot(x, y, 'o', label='original')
        pylab.plot(x, estimated_values, '-r', label='estimated')
        pylab.legend()
        pylab.xlabel("Years")
        pylab.ylabel("Celcius Degrees")
        rmse_value = rmse(y, estimated_values)
        title_string = "Celcius Degree vs Years \n RMSE = " + \
            str(rmse_value) + "\n" + \
            "Degree of the model = " + str(len(model)-1)
        pylab.title(title_string)
        pylab.grid()
        pylab.show()


if __name__ == '__main__':
    # x = pylab.array(range(50))
    # y = pylab.array(range(0, 100, 2))
    # degrees = [1, 2, 20]
    # models = generate_models(x, y, degrees)
    # evaluate_models_on_training(x, y, models)

    # Part A.4
    training_years_data = pylab.array(list(TRAINING_INTERVAL))
    length_of_data = len(TRAINING_INTERVAL)
    partA1_data = pylab.zeros(length_of_data)
    Climate_obj = Climate('data.csv')
    index1 = 0
    for index in TRAINING_INTERVAL:
        partA1_data[index1] = Climate_obj.get_daily_temp(
            'NEW YORK', 1, 10, index)
        index1 += 1
    linear_model = generate_models(training_years_data, partA1_data, [1])
    #evaluate_models_on_training(training_years_data, partA1_data, linear_model)

    partA2_data = pylab.zeros(length_of_data)
    index1 = 0
    for index in TRAINING_INTERVAL:
        partA2_data[index1] = pylab.mean(Climate_obj.get_yearly_temp(
            'NEW YORK', index))
        index1 += 1

    linear_model = generate_models(training_years_data, partA2_data, [1])
    #evaluate_models_on_training(training_years_data, partA2_data, linear_model)

    # COMMENTS:
    # What difference does choosing a specific day to plot the data for versus
    # calculating the yearly average have on our graphs (i.e., in terms of the R​2
    # values and the fit of the resulting curves)? Interpret the results.
    # ANSWER:
    # Oscillation and range of the data is decreased due to mean. R2 value is increased, which is good and expected.
    # Hence, fit of the curve is better.

    # Why do you think these graphs are so noisy? Which one is more noisy?
    # ANSWER:
    # Specific day data has more noise because daily weather conditions can heavily affect the observations.

    # How do these graphs support or contradict the claim that global warming is
    # leading to an increase in temperature? The slope and the standard
    # error-to-slope ratio could be helpful in thinking about this.
    # ANSWER:
    # As we can see from the plots, there is an increasing trend and standard error-to-slope ratio is lower for the less noisy data.

    # Part B
    partB_data = gen_cities_avg(Climate_obj, CITIES, training_years_data)
    linear_model = generate_models(training_years_data, partB_data, [1])
    #evaluate_models_on_training(training_years_data, partB_data, linear_model)

    # COMMENTS:
    # How does this graph compare to the graphs from part A ​(i.e., in terms of
    # the R​2​ values, the fit of the resulting curves, and whether the graph
    # supports/contradicts our claim about global warming)? Interpret the
    # results.
    # ANSWER:
    # Range of the data is lower for the part b and ratiof of SE is much lower than the ones in the part a. Hence, we can conclude that,
    # fitted line represents better the data for part B. Moreover, we can see that there is positive correlation between time and temperature which supports global warming claim.

    # Why do you think this is the case?
    # ANSWER:
    # Here we are actually observing more realizations(for every city) than the part A section 2; therefore, results are more reliable.

    # How would we expect the results to differ if we used 3 different cities?
    # What about 100 different cities?
    # ANSWER:
    # As the number of cities increases, our conclusion becomes more reliable because we observe more data.

    # How would the results have changed if all 21 cities were in the same region
    # of the United States?
    # ANSWER:
    # Results become biased because only one region can lead to wrong conclusions. Also, regional changes may be much more effictive for a specific region.

    # Part C
    window_size = 5
    averaged_data = moving_average(partB_data, window_size)
    part_C_model = generate_models(
        training_years_data, averaged_data, [1])
    # evaluate_models_on_training(
    #    training_years_data, averaged_data, part_C_model)
    # COMMENTS
    # How does this graph compare to the graphs from part A and B (​i.e., in
    # terms of the R​2​ values, the fit of the resulting curves, and whether the
    # graph supports/contradicts our claim about global warming)? Interpret the
    # results.
    # ANSWER
    # Reliability of the results are increased and graph supports the global warming cliam.
    # It is the case because moving average decreases the noise (low pass filter- cancels out high frequency noise).

    # Part D.2
    model_orders = [1, 2, 20]
    models = generate_models(training_years_data, averaged_data, model_orders)
    #evaluate_models_on_training(training_years_data, averaged_data, models)
    # COMMENTS
    # How do these models compare to each other?
    # Degree with 20 is the best and degree with 1 is the worst one, using lots of coefficients yield better results.
    # Which one has the best R2 ? Why?
    # Degree 20 has the best R2. Reason is that data is not exactly linear so a parabolic effect has resulted in better in terms of accuracy.
    # Which model best fits the data? Why?
    # Degree with 20 because it fits the data better with lots of coefficient.

    testing_years_data = pylab.array(list(TESTING_INTERVAL))
    testing_averaged_data = moving_average(gen_cities_avg(
        Climate_obj, CITIES, testing_years_data), window_size)
    # evaluate_models_on_testing(
    #     testing_years_data, testing_averaged_data, models)
    # COMMENTS
    # How did the different models perform? How did their RMSEs compare?
    # Linear model performed the best. As the model order increases, RMSE increases.
    # Which model performed the best? Which model performed the worst? Are
    # they the same as those in part D.2.I? Why?
    # As before mentioned, linear is the best. This is a great example of the overfitting. As we can see, model order 20 captures the training data best but it failed in the testing data.
    # If we had generated the models using the A.4.II data (i.e. average annual
    # temperature of New York City) instead of the 5-year moving average over
    # 22 cities, how would the prediction results 2010-2015 have changed?
    # It would be much less accurate because we smoothed the data by taking average which is a good thing for in case of outliers and noise and prediction according to less noisy data is better.

    # Part E
    std_deviations_training = moving_average(gen_std_devs(
        Climate_obj, CITIES, training_years_data), window_size)
    models_std = generate_models(
        training_years_data, std_deviations_training, [1, 2, 20])
    evaluate_models_on_training(
        training_years_data, std_deviations_training, models_std)
    # TODO: replace this line with your code
