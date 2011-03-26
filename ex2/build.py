#!/usr/bin/env python3

class Node:
    def __init__(self):
        self.executed=False
    def make_executed(self):
        if not self.executed:
            self.make_dependencies()
            if self.execute():
                print("Powłoka zwróciła informację o błędzie - przerywam!")
                exit(1)
        self.executed=True
        
build=[]

exec(open("project.py").read())

for v in build:
    if not isinstance(v,Node):
        print(v,"nie jest pochodną klasy Node")
        exit(1)
    v.make_executed()