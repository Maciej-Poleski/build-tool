# Kompiluje przykładową aplikacje z wykorzystaniem QtCore (HelloWorld)

import os

system=os.system

def debug_system(*args):
    """Sprawia że os.system() wysyła na wyjście swoje argumenty"""
    print(*args)
    system(*args)

os.system=debug_system

class DummyNode(Node):
    def execute(self):
        pass
    
class File(DummyNode):
    def __init__(self,name,*args):
        DummyNode.__init__(self,*args)
        self.file_name=name
    def get_directory(self):
        if os.path.dirname(self.file_name)=='':
            return '.'
        else:
            return os.path.dirname(self.file_name)
    def get_file(self):
        return os.path.basename(self.file_name)
    def executed(self):
        return os.access(self.file_name,os.R_OK)

class Source(File):
    pass

class CSource(Source):
    pass

class CxxSource(Source):
    pass

class Directory(DummyNode):
    def __init__(self,path,*args):
        Node.__init__(self,*args)
        self.path=path
        
class NewDirectory(Directory):
    def execute(self):
        os.system('mkdir -p '+self.path)

class IncludeDir(Directory):
    pass

class ObjectCode(File):
    def get_command_string(self):
        command_string=''
        for arg in self.args:
            if isinstance(arg,Helper):
                command_string+=' '+ObjectCode.get_command_string(arg)
            elif isinstance(arg,Source):
                command_string+=' '+arg.file_name
            elif isinstance(arg,IncludeDir):
                command_string+=' -I '+arg.path
            elif isinstance(arg,str) or isinstance(self,ObjectCode):
                command_string+=' '+arg
        return command_string
    def execute(self):
        command_args='-c -o '+self.file_name+' '+ObjectCode.get_command_string(self)
        os.system(self.get_command()+' '+command_args)

class CObjectCode(ObjectCode):
    def get_command(self):
        return 'gcc'

class CxxObjectCode(ObjectCode):
    def get_command(self):
        return 'g++'
        
class Library(File):
    pass

class SharedLibrary(Library):
    def get_command_string(self):
        command_string=''
        for arg in self.args:
            if isinstance(arg,Helper):
                command_string+=' '+SharedLibrary.get_command_string(arg)
            elif isinstance(arg,Source) or isinstance(arg,ObjectCode):
                command_string+=' '+arg.file_name
            elif isinstance(arg,SharedLibrary):
                command_string+=' -L '+arg.get_directory()+' -l '+arg.get_file()+' -Xlinker -rpath='+arg.get_directory()
            elif isinstance(arg,str) or isinstance(self,SharedLibrary):
                command_string+=' '+arg
        return command_string
    def execute(self):
        command_args='-shared -o '+self.file_name+' '+SharedLibrary.get_command_string(self)
        os.system(self.get_command()+' '+command_args)
    def get_file(self):
        return File.get_file(self)[3:-3]

class CSharedLibrary(SharedLibrary):
    def get_command(self):
        return 'gcc'

class CxxSharedLibrary(SharedLibrary):
    def get_command(self):
        return 'g++'

class Executable(File):
    def get_command_string(self):
        command_string=''
        for arg in self.args:
            if isinstance(arg,Helper):
                command_string+=' '+Executable.get_command_string(arg)
            elif isinstance(arg,Source) or isinstance(arg,ObjectCode):
                command_string+=' '+arg.file_name
            elif isinstance(arg,SharedLibrary):
                command_string+=' -L '+arg.get_directory()+' -l '+arg.get_file()+' -Xlinker -rpath='+arg.get_directory()
            elif isinstance(arg,str) or isinstance(self,Executable):
                command_string+=' '+arg
        return command_string
    def execute(self):
        command_args='-o '+self.file_name+' '+Executable.get_command_string(self)
        os.system(self.get_command()+' '+command_args)

class CExecutable(Executable):
    def get_command(self):
        return 'gcc'

class CxxExecutable(Executable):
    def get_command(self):
        return 'g++'

class Helper(DummyNode):
    pass

QtCore=Helper(CxxSharedLibrary('/usr/lib64/libQtCore.so'),IncludeDir('/usr/include'))

build.add(CxxExecutable('HelloWorld',QtCore,'main.cxx','HelloWorld.cxx'))