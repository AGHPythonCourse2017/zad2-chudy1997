import math
import numpy as np
import time
import logging
from complexity_estimate.UsageException import UsageException
from complexity_estimate.Timeout import timeout


def logger(func):
    logging.info("Running function " + str(func))
    return func


class ComplexCalc:
    logging.basicConfig(filename='ComplexCalc.log', level=logging.DEBUG)
    ind = 1
    complexities = {'O(logn)': lambda x: math.log2(x),
                    'O(nlogn)': lambda x: x * math.log2(x),
                    'O(n)': lambda x: x,
                    'O(n^2)': lambda x: math.pow(x, 2),
                    'O(n^3)': lambda x: math.pow(x, 3)}

    inverses = {'O(logn)': lambda x: int(math.pow(2, x)),
                'O(nlogn)': lambda x: x * math.log(2),
                'O(n)': lambda x: int(x),
                'O(n^2)': lambda x: int(math.pow(x, 1 / 2)),
                'O(n^3)': lambda x: int(math.pow(x, 1 / 3))}

    @staticmethod
    def w0(x):
        def fun(n): return n * math.log(n, 2) - x

        def deriv(n): return (math.log(n) + 1) / math.log(2)
        newton_val = x
        eps = 0.000001
        while fun(newton_val) / deriv(newton_val) > eps:
            newton_val = newton_val - (fun(newton_val) / deriv(newton_val))
        return newton_val

    def __init__(self, func, tab, base=2,
                 min_range=9, max_range=12, max_sec=30):
        self.complexity = None
        self.const = None
        self.func = func
        self.base = base
        self.min_range = min_range
        self.max_range = max_range
        self.max_sec = max_sec
        self.tab = tab
        logging.info(
            "Call no. " + str(ComplexCalc.ind) + " with args: " + "func=" +
            func.__name__ + " tab having length=" + str(len(tab)) +
            " base=" + str(base) + " min_range=" + str(min_range) +
            " max_range=" + str(max_range) + " timeout=" + str(max_sec))
        ComplexCalc.ind += 1

    @logger
    def calculate_times(self, send_end):
        times = np.zeros((self.max_range - self.min_range + 1, 2))
        for i in range(len(times)):
            ran = pow(self.base, self.min_range + i)
            start = time.time()
            self.func(self.tab[1:ran])
            times[i][0] = time.time() - start
            times[i][1] = ran
            send_end.send(times)

    @logger
    def calculate_std_dev(self, times):
        res = dict()
        for name, f in self.complexities.items():
            vals = []
            for tim, N in times:
                if f(N) != 0:
                    vals.append(tim / f(N))
            res[name] = (np.std(vals) / np.mean(vals), np.mean(vals))
        return res

    @staticmethod
    @logger
    def find_complexity(dev_mean):
        compl = ('', float('inf'), 0)
        for n, (s, c) in dev_mean.items():
            if s < compl[1]:
                compl = (n, s, c)
        return compl

    @logger
    def calculate_complexity(self):
        times = timeout(self.calculate_times, self.max_sec)
        dev_mean = self.calculate_std_dev(times)
        compl = self.find_complexity(dev_mean)
        self.complexity = compl[0]
        self.const = compl[2]
        logging.info("Supposed complexity: " + str(self.complexity))
        print("Supposed complexity: ", self.complexity, '\n')

    @logger
    def get_time_foreseer(self):
        def res(n):
            logging.info("Calculating time for size " + str(n))
            if not self.complexity:
                logging.error("Bad usage: Cannot foresee "
                              "time before calculating complexity")
                raise UsageException("Cannot foresee "
                                     "time before calculating complexity")
            print("For size = ", n)
            return time_foresee(n)

        def time_foresee(n):
            tmp = self.complexities[self.complexity](n) * self.const
            print("possible time = ", int(tmp))
            return tmp

        return res

    @logger
    def get_size_foreseer(self):
        def res(n):
            logging.info("Calculating size for time " + str(n))
            if not self.complexity:
                logging.error("Bad usage: Cannot foresee "
                              "size before calculating complexity")
                raise UsageException("Cannot foresee "
                                     "size before calculating complexity")
            print("For time = ", n)
            return size_foresee(n)

        def size_foresee(tim):
            if self.complexity != "O(nlogn)":
                tmp = self.inverses[self.complexity](tim / self.const)
            else:
                tmp = ComplexCalc.w0(tim / self.const)
            print("possible size = ", int(tmp))
            return tmp

        return res
