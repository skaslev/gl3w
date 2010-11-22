import os, shutil

env = Environment()
if env.GetOption('clean'):
    for d in ['bin', 'include', 'lib']:
        shutil.rmtree(d, True)
    try: os.unlink('src/gl3w.c')
    except: pass
else:
    print 'Generating gl3w...'
    execfile('gl3w_gen.py')

env.Append(CFLAGS=['-Wall', '-O2'])
env.Append(CPPPATH='include')
env.SharedLibrary('lib/gl3w', 'src/gl3w.c')
o = env.Object('src/test', 'src/test.c')
env.Program('bin/test_static', [o, 'src/gl3w.c'], LIBS='glut')
env.Program('bin/test_shared', o, LIBS=['gl3w', 'glut'],
            LIBPATH='lib', RPATH=os.path.abspath('lib'))
