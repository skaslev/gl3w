#!/usr/bin/env python
import re
import os
import urllib2

# Create directories
if not os.path.exists('include/GL3'):
    os.makedirs('include/GL3')
if not os.path.exists('src'):
    os.makedirs('src')

# Download gl3.h
if not os.path.exists('include/GL3/gl3.h'):
    web = urllib2.urlopen('http://www.opengl.org/registry/api/gl3.h')
    with open('include/GL3/gl3.h', 'wb') as f:
        f.writelines(web.readlines())

# Parse function names from gl3.h
procs = []
p = re.compile(r'GLAPI.*APIENTRY\s+(\w+)')
with open('include/GL3/gl3.h', 'r') as f:
    for line in f:
        m = p.match(line)
        if m:
            procs.append(m.group(1))

def proc_t(proc):
    return {'p': proc, 'p_t': 'PFN' + proc.upper() + 'PROC'}

# Generate gl3w.h
with open('include/GL3/gl3w.h', 'wb') as f:
    f.write(r'''#ifndef __gl3w_h_
#define __gl3w_h_

#include <GL3/gl3.h>

#ifndef __gl_h_
#define __gl_h_
#endif

#ifdef __cplusplus
extern "C" {
#endif

int gl3wInit(void);

/* GL functions */
''')
    for proc in procs:
        f.write('extern %(p_t)s %(p)s;\n' % proc_t(proc))
    f.write(r'''
#ifdef __cplusplus
}
#endif

#endif
''')

# Generate gl3w.c
with open('src/gl3w.c', 'wb') as f:
    f.write(r'''#include <GL3/gl3w.h>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN 1
#include <windows.h>

static HANDLE libgl;

static void open_libgl(void)
{
	libgl = LoadLibrary("opengl32.dll");
}

static void close_libgl(void)
{
	FreeLibrary(libgl);
}

static void *get_proc(const char *proc)
{
	void *res;
	res = wglGetProcAddress(proc);
	if (!res)
		res = GetProcAddress(libgl, proc);
	return res;
}
#else
#include <dlfcn.h>
#include <GL/glx.h>

static void *libgl;

static void open_libgl(void)
{
	libgl = dlopen("libGL.so.1", RTLD_LAZY | RTLD_GLOBAL);
}

static void close_libgl(void)
{
	dlclose(libgl);
}

static void *get_proc(const char *proc)
{
	void *res;
	res = glXGetProcAddress((const GLubyte *) proc);
	if (!res)
		res = dlsym(libgl, proc);
	return res;
}
#endif

''')
    for proc in procs:
        f.write('%(p_t)s %(p)s;\n' % proc_t(proc))
    f.write(r'''

int gl3wInit(void)
{
	open_libgl();

''')
    for proc in procs:
        f.write('\t%(p)s = (%(p_t)s) get_proc("%(p)s");\n' % proc_t(proc))
    f.write(r'''
	close_libgl();
	return 1;
}
''')
