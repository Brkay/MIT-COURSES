def month_calculator(annual_salary, portion, total_cost, semi_annual_raise):
    portion_down_payment = 0.25# Down payment (Peşinat)
    monthly_salary = annual_salary / 12.0
    down_payment_cost = total_cost * portion_down_payment
    monthly_savings = monthly_salary*portion
    current_savings = 0.0
    r = 0.04 # Annual return.
    total_month = 0;
    while (current_savings < down_payment_cost):
        current_savings += current_savings*r / 12
        current_savings += monthly_savings
        total_month += 1
        if (total_month) % 6 == 0  and total_month != 0:
            annual_salary += annual_salary* semi_annual_raise
            monthly_savings = annual_salary / 12.0 * portion


    return total_month






if __name__ == "__main__":
    annual_salary = float(input("Please enter your annual salary:\n"))
    portion = float(input("Please enter the portion of salary to be saved:\n"))
    total_cost = float(input("Please enter the cost of your dream home:\n"))
    semi_annual_raise = float(input("Please enter the semi-annual salary raise:\n"))
    print(str( month_calculator(annual_salary, portion, total_cost, semi_annual_raise)) + " is the required months to save up enough money!")







#120000
#.10
#1000000

#80000
#.15
#500000
