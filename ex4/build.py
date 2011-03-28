#!/usr/bin/env python3

class Node:
    def __init__(self,*args):
        self.__executed=False
        self.args=args
    def executed(self):
        return False
    def make_dependencies(self):
        for arg in self.args:
            if isinstance(arg,Node):
                arg.make_executed()
    def add_args(self,*args):
        self.args.extend(args)
    def make_executed(self):
        if not self.__executed and not self.executed():
            self.make_dependencies()
            if self.execute():
                print("Powłoka zwróciła informację o błędzie - przerywam!")
                exit(1)
        self.__executed=True
        
build=set()
install=set()

exec(open("project.py").read())

for v in build:
    if not isinstance(v,Node):
        print(v,"nie jest pochodną klasy Node")
        exit(1)
    v.make_executed()