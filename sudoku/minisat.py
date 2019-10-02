import subprocess

class BoolVars(object):
    def __init__(self):
        """ Initialize and reset this instance """
        self.varList = {}
        return

    def add(self, name):
        """ Add an variable to the list """
        self.varList[name] = len(self.varList) + 1
        return

    def __len__(self):
        return len(self.varList)

    def __getitem__(self, name):
        if name in self.varList:
            return self.varList[name]
        else:
            raise MiniSatException("No such variable `{}`".format(name))

class Solver(object):
    def __init__(self, variable, binpath=None):
        """ Initialize and reset this instance """
        # search for minisat path
        if binpath is None:
            proc = subprocess.run(['/usr/bin/which', 'minisat'],
                                  stdout=subprocess.PIPE)
            self.binpath = proc.stdout.rstrip(b'\n').decode()
            if self.binpath == '':
                raise MiniSatException("Could not find `minisat`")
        else:
            self.binpath = binpath

        # check for variable
        if isinstance(variable, BoolVars):
            self.variable = variable
        else:
            raise MiniSatException("Expected `BoolVars` but `{}` given".format(variable))

        self.closureList = []
        return

    def add(self, closure):
        """ Add a closure """
        if not isinstance(closure, list):
            raise MiniSatException("Closure must be a list")
        self.closureList.append(closure)
        return

    def solve(self, variable,
              inFile='/tmp/minisat_input.txt',
              outFile='/tmp/minisat_output.txt'):
        """ Solve the equation """
        # write input file
        with open(inFile, 'w') as f:
            f.write('p cnf {} {}\n'.format(
                len(variable), len(self.closureList)
            ))
            for closure in self.closureList:
                for var in closure:
                    f.write('{} '.format(var))
                else:
                    f.write('0\n')

        # run minisat
        proc = subprocess.run([self.binpath, inFile, outFile],
                              stdout = subprocess.PIPE)

        # read output file
        model = Model(variable)
        with open(outFile, 'r') as f:
            judge = f.readline().rstrip('\n')
            if judge == 'SAT':
                model.judge = True
                l = f.readline().rstrip('\n')
                model.load(
                    list(map(int, l.split(' ')))[::-1]
                )
            else:
                model.judge = False
        return model

    def Not(self, val):
        return -val

class Model(object):
    def __init__(self, variable):
        """ Reset and initialize this instance """
        self.variable = variable
        self.judge = False
        self.solution = {}
        return

    def is_sat(self):
        return self.judge

    def load(self, result):
        """ Read the output of MiniSat and map them to BoolVars variables """
        for key in self.variable.varList:
            i = self.variable.varList[key]
            for elm in result:
                if abs(elm) == i:
                    if elm < 0:
                        self.solution[key] = False
                    else:
                        self.solution[key] = True
                    break
        return

    def __getitem__(self, name):
        if name in self.solution:
            return self.solution[name]
        else:
            raise MiniSatException("No such variable `{}`".format(name))

class MiniSatException(Exception):
    pass
