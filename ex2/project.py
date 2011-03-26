import os

# STUB!!!!!

# Zestaw klas służących do kompilacji kilku plików ANSI C do postaci
# biblioteki współdzielonej (so) oraz wykorzystanie jej w przykładowej
# aplikacji (obsługiwany Toolchain to: pc-linux-gnu-*)

class Source(Node):
    def __init__(self,file):
        Node.__init__(self)
        self.__file_name=file
        self.__includes=set()
        self.__libraries=set()
        self.__compile_flags=[]
    
    def add_includes(self,includes):
        self.__includes=self.__includes|includes
    
    def add_libraries(self,libraries):
        self.__libraries=self.__libraries|libraries
        
    def add_compile_flags(self,flags):
        self.__compile_flags.extend(flags)
    
    def get_file_name(self):
        return self.__file_name
    
    def get_includes(self):
        return self.__includes
    
    def get_libraries(self):
        return self.__libraries
    
    def get_compile_flags(self):
        return self.__compile_flags
    
    def make_dependencies(self):
        pass
    
    def execute(self):
        pass
    
class CSource(Source):
    def __init__(self,file):
        Source.__init__(self,file)

class CxxSource(Source):
    def __init__(self,file):
        Source.__init__(self,file)
        
class ObjectCode(Node):
    def __init__(self,output_file):
        Node.__init__(self)
        self.__input_files=set()
        self.__output_file=output_file
    
    def make_dependencies(self):
        for dependency in self.__input_files:
            dependency.make_executed()
    
    def add_input_files(self,input_files):
        self.__input_files=self.__input_files|input_files
        
    def get_output_file(self):
        return self.__output_file
    
    def get_input_files(self):
        return self.__input_files
        
    def get_compiler_args(self):
        command=' -c -o '+self.get_output_file()
        includes=set()
        compile_flags=[]
        input_files=[]
        for input_file in self.__input_files:
            includes=includes|input_file.get_includes()
            compile_flags.extend(input_file.get_compile_flags())
            input_files.append(input_file.get_file_name())
        
        for flag in compile_flags:
            command+=' '+flag
        
        for include in includes:
            command+=' -I'+include
        
        for file in input_files:
            command+=' '+file
        
        return command
        
class CObjectCode(ObjectCode):
    def __init__(self,output_file):
        ObjectCode.__init__(self,output_file)
    
    def execute(self):
        print('C',{file.get_file_name() for file in self.get_input_files()},'->',self.get_output_file())
        os.system('gcc'+self.get_compiler_args())
                
class CxxObjectCode(ObjectCode):
    def __init__(self,output_file):
        ObjectCode.__init__(self,output_file)
    def execute(self):
        print('CXX',{file.get_file_name() for file in self.get_input_files()},'->',self.get_output_file())
        os.system('g++'+self.get_compiler_args())
                        
class Library:
    def __init__(self,path,name):
        self.path=path
        self.name=name

    def get_path(self):
        return self.path

    def get_name(self):
        return self.name


class SharedLibrary:
    pass

class Executable:
    pass

# TODO:
# Model: Parser sekwencyjny drzewiasty
# Przy dodawaniu zależności obsługujemy konkretne akcje
# Klasa (obiekt) "wie" jakie są potrzebne dodatkowe flagi dla poszczególnych
#  akcji.
# Konstruktor przyjmuje output (input tylko w wyjątkowych sytuacjach), flagi
#  najprawdopodobniej styl mieszany

a_c=CSource('a.c')
b_c=CSource('b.c')
x_c=CSource('x.c')

a_c.add_compile_flags(["-O2","-Wall"])
b_c.add_compile_flags(["-O2","-Wall"])
x_c.add_compile_flags(["-O2","-Wall"])

a_o=CObjectCode('a.o')
b_o=CObjectCode('b.o')
x_o=CObjectCode('x.o')

a_o.add_input_files({a_c})
b_o.add_input_files({b_c})
x_o.add_input_files({x_c})

build.append(a_o)
build.append(b_o)
build.append(x_o)
