import sys


class Config(object):
    def __init__(self, configfile):
        self.configfile = configfile
        self.config = {}
        try:
            with open(self.configfile, 'r') as f:
                for l in f:
                    items = l.split('=')
                    key = items[0].strip()
                    value = items[1].strip()
                    self.config[key] = float(value)
        except Exception as e:
            raise e
        f.close()

    def get_config(self):
        return self.config


class UserData(object):
    def __init__(self, userdatafile):
        self.userdatafile = userdatafile
        self.user = {}
        try:
            with open(self.userdatafile, 'r') as f:
                for l in f:
                    items = l.split(',')
                    key = items[0].strip()
                    value = items[1].strip()
                    self.user[key] = float(value)
        except Exception as e:
            raise e

    def get_user(self):
        return self.user

    def s_s(self, rate, salary):

            if salary <= 2193:
                ss = 2193 * rate
            elif salary > 16446:
                ss = 16446 * rate
            else:
                ss = salary * rate
            return ss

    def t_s(self, salary, ss):
        ts = salary - ss - 3500
        if ts <= 0:
            tax = ss
        elif ts <= 1500:
            tax = ts * 0.03 - 0
        elif ts <= 4500:
            tax = ts * 0.1 - 105
        elif ts <= 9000:
            tax = ts * 0.2 - 555
        elif ts <= 35000:
            tax = ts * 0.25 - 1005
        elif ts <= 55000:
            tax = ts * 0.3 - 2755
        elif ts <= 80000:
            tax = ts * 0.35 - 5505
        else:
            tax = ts * 0.45 - 13505
        return tax


if __name__ == "__main__":
    # args = sys.argv[1:]
    # index = args.index('-c')
    # configfile = args[index + 1]
    # index = args.index('-d')
    # userdatafile = args[index + 1]
    # index = args.index('-o')
    # ofile = args[index + 1]
    configfile = 'test.cfg'
    userdatafile = 'salary.csv'
    ofile = 'output.csv'
    C = Config(configfile)
    rate = sum(list(C.get_config().values())[2:])
    U = UserData(userdatafile)
    user = U.get_user()
    for key, value in user.items():
        salary = int(value)
        id = int(key)
        ss = U.s_s(rate, salary)
        tax = U.t_s(salary, ss)
        income = salary - ss - tax
        try:
            with open(ofile, 'a') as f:
                f.write("%d,%d,%.2f,%.2f,%.2f" % (id, salary, ss, tax, income))
                f.write('\n\n')
        except Exception as e:
            raise e
        f.close()