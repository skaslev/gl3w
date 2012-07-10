import os, shutil, platform

env = Environment()
if env.GetOption('clean'):
    for d in ['bin', 'include', 'lib']:
        shutil.rmtree(d, True)
    try: os.unlink('src/gl3w.c')
    except: pass
else:
    print 'Generating gl3w...'
    execfile('gl3w_gen.py')

if platform.system() == 'Darwin':
    env.Append(CFLAGS=['-I/sw/include', '-I/opt/local/include', '-I/usr/X11/include'])
    env.Append(LINKFLAGS=['-L/sw/lib', '-I/opt/local/lib'])
    env.Append(FRAMEWORKS=['CoreFoundation'])

env.Append(CFLAGS=['-Wall', '-O2'])
env.Append(CPPPATH='include')
env.SharedLibrary('lib/gl3w', 'src/gl3w.c')
o = env.Object('src/test', 'src/test.c')
env.Program('bin/test_static', [o, 'src/gl3w.c'], LIBS='glut')
env.Program('bin/test_shared', o, LIBS=['gl3w', 'glut'],
            LIBPATH='lib', RPATH=os.path.abspath('lib'))
