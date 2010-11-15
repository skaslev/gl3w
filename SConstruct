import os

for f in ['include/GL3/gl3.h', 'include/GL3/gl3w.h', 'src/gl3w.c']:
    try: os.unlink(f)
    except: pass

env = Environment()
if not env.GetOption('clean'):
    print 'generating gl3w...'
    execfile('gl3w_gen.py')

env.Append(CFLAGS=['-Wall', '-O2'])
env.Append(CPPPATH='include')
env.SharedLibrary('bin/gl3w', 'src/gl3w.c')
o = env.Object('src/test', 'src/test.c')
env.Program('bin/test_static', [o, 'src/gl3w.c'], LIBS='glut')
env.Program('bin/test_shared', o, LIBS=['gl3w', 'glut'], LIBPATH='bin', RPATH=['.', 'bin'])
