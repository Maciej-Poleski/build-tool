#include <QtCore/QCoreApplication>
#include "HelloWorld.hxx"

int main(int argc,char**argv)
{
    QCoreApplication app(argc,argv);
    HelloWorld *helloWorld=new HelloWorld();
    delete helloWorld;
    app.exit(0);
    return app.exec();
}