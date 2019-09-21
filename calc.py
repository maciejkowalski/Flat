import math
import plotly
import sys
import argparse
import plotly.graph_objects as go
from enum import Enum

class InstallmentType(Enum):
    def __str__(self):
        return str(self.value)
    equal_type       = "equal"
    decreasing_type  = "decreasing"
    
    @staticmethod
    def from_str(label):
        if label == str(InstallmentType.equal_type):
            return InstallmentType.equal_type
        elif label == str(InstallmentType.decreasing_type):
            return InstallmentType.decreasing_type
        else:
            raise "Error::InstallmentType: label not supported"

class Mortgage_cal:
    def __init__(self, 
                 loan_value: int, 
                 interest_rate: int, 
                 wibor_rate: int, 
                 period_year: int,
                 installment_type: InstallmentType):
        self.loan_value = loan_value
        self.interest_rate = interest_rate
        self.wibor_rate = wibor_rate
        self.period_year = period_year
        self.installment_type = installment_type
        
        self.nominal_interest_year = (self.wibor_rate+interest_rate)/100
        self.nominal_interest_msc = self.nominal_interest_year/12
        
    def get_installment_equal_value(self):
        value = self.loan_value * (self.nominal_interest_msc*pow((1+self.nominal_interest_msc), \
                self.period_year*12))/(pow((1+self.nominal_interest_msc),self.period_year*12)-1)
        return value
    
    def get_balance(self):
        time_vector = []
        capital_sum_vector = []
        costs_sum_vector = []
        capital_part_vector = []
        costs_part_vector = []

        capital_paid_sum_tmp = 0
        costs_sum_tmp = 0
        if self.installment_type is InstallmentType.decreasing_type:
            for i in range(1, 12*self.period_year + 1):
                capital_paid = (self.loan_value/(12*self.period_year))
                costs = (self.loan_value - i*capital_paid)*(self.nominal_interest_msc)
                capital_paid_sum_tmp = capital_paid_sum_tmp + capital_paid
                costs_sum_tmp = costs_sum_tmp + costs
                
                time_vector.append(i)
                capital_sum_vector.append(capital_paid_sum_tmp)
                costs_sum_vector.append(costs_sum_tmp)
                capital_part_vector.append(capital_paid)
                costs_part_vector.append(costs)
        elif self.installment_type is InstallmentType.equal_type:
            installment_equal = self.get_installment_equal_value()
            
            capital_to_pay = self.loan_value
            for i in range(1, 12*self.period_year + 1):
                costs = capital_to_pay*self.nominal_interest_msc
                costs_sum_tmp = costs_sum_tmp + costs
                capital_paid = installment_equal - costs
                capital_paid_sum_tmp = capital_paid_sum_tmp + capital_paid
                capital_to_pay = capital_to_pay - capital_paid
                
                time_vector.append(i)
                capital_sum_vector.append(capital_paid_sum_tmp)
                costs_sum_vector.append(costs_sum_tmp)
                capital_part_vector.append(capital_paid)
                costs_part_vector.append(costs)
        else:
            raise "Error::Mortgage_cal:Installment type not supported. Check parameters"
                
        return time_vector, capital_sum_vector, costs_sum_vector, capital_part_vector, costs_part_vector
            
    def plot_simulation_graph(self):
        time, capital_sum, costs_sum, capital_part, costs_part = self.get_balance()
        
        #figure 1
        fig1 = go.Figure(data=[
                go.Bar(name='capital', x=time, y=capital_part),
                go.Bar(name='cost',    x=time, y=costs_part)])
        fig1.update_layout(barmode='stack', title="mortgage_part:"+str(self.installment_type))
        fig1.show()

        #figure 2
        fig2 = go.Figure(data=[
                        go.Bar(name='capital_sum', x=time, y=capital_sum),
                        go.Bar(name='cost_sum',    x=time, y=costs_sum)])
        fig2.update_layout(barmode='stack', title="mortgage_sum:"+str(self.installment_type))
        fig2.show()


if __name__ == '__main__':
    arg = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parameters = parser.add_argument_group("loan_param")
    parameters.add_argument("-l",  "--loan",             help="Amount of credit [ex. 300000]",           type=int, required=True)
    parameters.add_argument("-bi", "--bank_interest",    help="Bank interest [ex. 2%]",                  type=int, required=True)
    parameters.add_argument("-w",  "--wibor",            help="Warsaw Interbank Offered Rate [ex. 2%]",  type=int, required=True)
    parameters.add_argument("-y",  "--loan_diuration",   help="A loan duration [ex. 20 year]",           type=int, required=True)
    parameters.add_argument("-it", "--installment_type", help="An installement type [equal/decreasing]", type=str, required=True)

    args = parser.parse_args(arg)
    
    calc = Mortgage_cal(args.loan, args.bank_interest, args.wibor, args.loan_diuration, InstallmentType.from_str(args.installment_type))
    calc.plot_simulation_graph()
