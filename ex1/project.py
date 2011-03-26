import os

# Klasa służąca do kompilacji przykładowego pliku ANSI C przy użyciu GCC

class GccCompileOneSource(Node):
    def __init__(self,input,output,flags=""):
        Node.__init__(self)
        self.input=input
        self.output=output
        self.flags=flags
    def make_dependencies(self):
        pass
    def execute(self):
        print("Kompilacja:",self.input,"->",self.output)
        return os.system("gcc "+self.flags+" "+self.wrap_input(self.input)+" "+self.wrap_output(self.output))
    def wrap_input(self,input):
        return input
    def wrap_output(self,output):
        return "-o "+output

build.append(GccCompileOneSource("main.c","test","-O2 -Wall -fomit-frame-pointer"))