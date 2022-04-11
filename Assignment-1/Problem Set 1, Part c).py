semi_annual_raise = 0.07
portion_down_payment = 0.25# Down payment (Peşinat)
total_cost = 1E6
total_month = 36
down_payment_cost = total_cost * portion_down_payment
r = 0.04
def month_calculator(annual_salary,portion):
    monthly_salary = annual_salary / 12.0
    monthly_savings = monthly_salary*portion
    calculated_month = 0
    current_savings = 0.0
    while (abs(current_savings - down_payment_cost) > 100 and current_savings <= down_payment_cost):
        current_savings += current_savings*r / 12
        current_savings += monthly_savings
        calculated_month += 1
        if (calculated_month) % 6 == 0  and calculated_month != 0:
            annual_salary += annual_salary* semi_annual_raise
            monthly_savings = annual_salary / 12.0 * portion

    return calculated_month


def portion_calculator(annual_salary):
    min_interval_int = 0 # a
    max_interval_int = 10000 # b
    bisection_search = 2
    f_b = month_calculator(annual_salary, max_interval_int / 10000.0)
    c = (min_interval_int + max_interval_int) / 2.0
    f_c = month_calculator(annual_salary,c / 10000.0)
    if f_b > total_month:
        print("There is no such a possibility")
        return 0, bisection_search

    while(f_c  != total_month):
        print(f_c)
        bisection_search += 1
        if f_c - total_month  > 0:
            min_interval_int = c
            c = ( min_interval_int + max_interval_int) / 2.0
            f_c = month_calculator(annual_salary,c / 10000.0)
        else:
            max_interval_int = c
            c = (min_interval_int + max_interval_int) / 2.0
            f_c = month_calculator(annual_salary,c/10000.0)
    return c/10000.0,bisection_search







if __name__ == "__main__":
    annual_salary = float(input("Please enter your annual salary:\n"))
    outputs = portion_calculator(annual_salary)
    print(str(outputs[0]) + " is the required rate of savings to save up enough money!")
    print(str(outputs[1]) + " search number")






#120000
#.10
#1000000

#80000
#.15
#500000
