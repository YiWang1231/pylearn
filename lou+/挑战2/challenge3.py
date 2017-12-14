import sys
from collections import namedtuple
import csv

# type + collections
IncomeTaxQuickLookUpItem = namedtuple('IncomeTaxQuickLookUpItem', ['start_point', 'tax_rate', 'quick_subtractor'])

Income_Tax_Start_Point = 3500
Income_Tax_Quick_Lookup_Table = [
    IncomeTaxQuickLookUpItem(80000, 0.45, 13505),
    IncomeTaxQuickLookUpItem(55000, 0.35, 5505),
    IncomeTaxQuickLookUpItem(35000, 0.30, 2755),
    IncomeTaxQuickLookUpItem(9000, 0.25, 1005),
    IncomeTaxQuickLookUpItem(4500, 0.2, 555),
    IncomeTaxQuickLookUpItem(1500, 0.1, 105),
    IncomeTaxQuickLookUpItem(0, 0.03, 0)
]


class Args(object):
    def __init__(self):
        self.args = sys.argv[1:]

    def _value_after_option(self, option):
        try:
            index = self.args.index(option)#获取参数的索引
            return self.args[index + 1]
        except(ValueError, IndexError):
            print('Parameter Error')
            exit()
    @property
    def config_path(self):
        return self._value_after_option('-c')

    @property
    def userdata_path(self):
        return self._value_after_option('-d')

    @property
    def out_file(self):
        return self._value_after_option('-o')


args = Args()


class Config(object):
    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config_path = args.config_path
        config = {}
        with open(config_path, 'r') as f:
            for l in f:
                items = l.split('=')
                try:
                    config[items[0].strip()] = float(items[1].strip())
                except ValueError:
                    print('Parameter Error')
        return config

    def _get_config(self, key):
        try:
            return self.config[key]
        except KeyError:
            print('config error')
            exit()

    @property# 有什么作用
    def social_security_low(self):
        return self._get_config('JiShuL')

    @property
    def social_security_high(self):
        return self._get_config('JiShuH')

    @property
    def social_security_rate(self):
        return sum([
            self._get_config('YangLao'),
            self._get_config('YiLiao'),
            self._get_config('ShiYe'),
            self._get_config('ShengYu'),
            self._get_config('GongJiJin')
        ])


config = Config()


class UserData(object):
    def __init__(self):
        self.userdata = self._read_users_data()

    def _read_users_data(self):
        userdata_path = args.userdata_path#属性不需要加括号 直接引用
        userdata = []
        with open(userdata_path, 'r') as f:
            for l in f:
                employee_id, income_string = l.strip().split(',')
                try:
                    income = int(income_string)
                except ValueError:
                    print('Parameter Error')
                    exit()
                userdata.append((employee_id, income))
        return userdata

    def __iter__(self):
        return iter(self.userdata)


class IncomeTaxCalculator(object):
    def __init__(self, userdata):
        self.userdata = userdata

    @staticmethod
    def cal_social_security_insurance_money(income):
        if income < config.social_security_low:
            return config.social_security_low * config.social_security_rate
        if income > config.social_security_high:
            return config.social_security_high * config.social_security_rate

        return income * config.social_security_rate

    @classmethod
    def cal_income_tax_and_remain(cls, income):
        social_security_insurance = cls.cal_social_security_insurance_money(income)
        real_income = income - social_security_insurance
        tax_part = real_income - Income_Tax_Start_Point
        if tax_part <= 0:
            return '0.00', '{:.2f}'.format(real_income)
        for item in Income_Tax_Quick_Lookup_Table:
            if tax_part > item.start_point:
                tax = tax_part * item.tax_rate - item.quick_subtractor
                return '{:.2f}'.format(tax), '{:.2f}'.format(real_income-tax)

    def cal_user_for_all(self):
        result = []
        for employee_id, income in self.userdata:
            data = [employee_id, income]
            social_insurance_money = '{:.2f}'.format(self.cal_social_security_insurance_money(income))
            tax, remain = self.cal_income_tax_and_remain(income)
            data += [social_insurance_money, tax, remain]
            result.append(data)
        return result

    def export(self, default='csv'):

        result = self.cal_user_for_all()
        with open(args.out_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(result)


if __name__ == "__main__":
    calculator = IncomeTaxCalculator(UserData())
    calculator.export()