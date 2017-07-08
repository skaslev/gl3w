import os
import platform
import shutil

env = Environment()
if env.GetOption('clean'):
    for d in ['bin', 'include', 'lib']:
        shutil.rmtree(d, True)
    try:
        os.unlink('src/gl3w.c')
    except:
        pass
else:
    print 'Generating gl3w...'
    os.system('./gl3w_gen.py')

libs = []
if platform.system() == 'Darwin':
    env.Append(CFLAGS=['-Wno-deprecated-declarations'],
               FRAMEWORKS=['GLUT'])
else:
    libs = ['glut', 'dl']

env.Append(CFLAGS=['-Wall', '-Wextra', '-pedantic', '-O2'])
env.Append(CPPPATH='include')
env.SharedLibrary('lib/gl3w', 'src/gl3w.c')
o = env.Object('src/glut_test', 'src/glut_test.c')
env.Program('bin/glut_test_static', [o, 'src/gl3w.c'], LIBS=libs)
env.Program('bin/glut_test_shared', o, LIBS=libs + ['gl3w'],
            LIBPATH='lib', RPATH=os.path.abspath('lib'))
