#!/usr/bin/env python

# Allow Python 2.6+ to use the print() function
from __future__ import print_function

import re
import os

# Try to import Python 3 library urllib.request
# and if it fails, fall back to Python 2 urllib2
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2

# Create directories
if not os.path.exists('include/GL'):
    os.makedirs('include/GL')
if not os.path.exists('src'):
    os.makedirs('src')

# Download glcorearb.h
if not os.path.exists('include/GL/glcorearb.h'):
    print('Downloading glcorearb.h to include/GL...')
    web = urllib2.urlopen('http://www.opengl.org/registry/api/glcorearb.h')
    with open('include/GL/glcorearb.h', 'wb') as f:
        f.writelines(web.readlines())
else:
    print('Reusing glcorearb.h from include/GL...')

# Parse function names from glcorearb.h
print('Parsing glcorearb.h header...')
procs = []
p = re.compile(r'GLAPI.*APIENTRY\s+(\w+)')
with open('include/GL/glcorearb.h', 'r') as f:
    for line in f:
        m = p.match(line)
        if m:
            procs.append(m.group(1))

def proc_t(proc):
    return { 'p': proc,
             'p_s': 'gl3w' + proc[2:],
             'p_t': 'PFN' + proc.upper() + 'PROC' }

# Generate gl3w.h
print('Generating gl3w.h in include/GL...')
with open('include/GL/gl3w.h', 'wb') as f:
    f.write(br'''#ifndef __gl3w_h_
#define __gl3w_h_

#include <GL/glcorearb.h>

#ifndef __gl_h_
#define __gl_h_
#endif

#ifdef __cplusplus
extern "C" {
#endif

typedef void (*GL3WglProc)(void);

/* gl3w api */
int gl3wInit(void);
int gl3wIsSupported(int major, int minor);
GL3WglProc gl3wGetProcAddress(const char *proc);

/* OpenGL functions */
''')
    for proc in procs:
        f.write('extern {0[p_t]} {0[p_s]};\n'.format(proc_t(proc)).encode("utf-8"))
    f.write(b'\n')
    for proc in procs:
        f.write('#define {0[p]}\t\t{0[p_s]}\n'.format(proc_t(proc)).encode("utf-8"))
    f.write(br'''
#ifdef __cplusplus
}
#endif

#endif
''')

# Generate gl3w.c
print('Generating gl3w.c in src...')
with open('src/gl3w.c', 'wb') as f:
    f.write(br'''#include <GL/gl3w.h>

#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN 1
#include <windows.h>

static HMODULE libgl;

static void open_libgl(void)
{
	libgl = LoadLibraryA("opengl32.dll");
}

static void close_libgl(void)
{
	FreeLibrary(libgl);
}

static GL3WglProc get_proc(const char *proc)
{
	GL3WglProc res;

	res = (GL3WglProc) wglGetProcAddress(proc);
	if (!res)
		res = (GL3WglProc) GetProcAddress(libgl, proc);
	return res;
}
#elif defined(__APPLE__) || defined(__APPLE_CC__)
#include <Carbon/Carbon.h>

CFBundleRef bundle;
CFURLRef bundleURL;

static void open_libgl(void)
{
	bundleURL = CFURLCreateWithFileSystemPath(kCFAllocatorDefault,
		CFSTR("/System/Library/Frameworks/OpenGL.framework"),
		kCFURLPOSIXPathStyle, true);

	bundle = CFBundleCreate(kCFAllocatorDefault, bundleURL);
	assert(bundle != NULL);
}

static void close_libgl(void)
{
	CFRelease(bundle);
	CFRelease(bundleURL);
}

static GL3WglProc get_proc(const char *proc)
{
	GL3WglProc res;

	CFStringRef procname = CFStringCreateWithCString(kCFAllocatorDefault, proc,
		kCFStringEncodingASCII);
	res = (GL3WglProc) CFBundleGetFunctionPointerForName(bundle, procname);
	CFRelease(procname);
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

static GL3WglProc get_proc(const char *proc)
{
	GL3WglProc res;

	res = (GL3WglProc) glXGetProcAddress((const GLubyte *) proc);
	if (!res)
		res = (GL3WglProc) dlsym(libgl, proc);
	return res;
}
#endif

static struct {
	int major, minor;
} version;

static int parse_version(void)
{
	if (!glGetIntegerv)
		return -1;

	glGetIntegerv(GL_MAJOR_VERSION, &version.major);
	glGetIntegerv(GL_MINOR_VERSION, &version.minor);

	if (version.major < 3)
		return -1;
	return 0;
}

static void load_procs(void);

int gl3wInit(void)
{
	open_libgl();
	load_procs();
	close_libgl();
	return parse_version();
}

int gl3wIsSupported(int major, int minor)
{
	if (major < 3)
		return 0;
	if (version.major == major)
		return version.minor >= minor;
	return version.major >= major;
}

GL3WglProc gl3wGetProcAddress(const char *proc)
{
	return get_proc(proc);
}

''')
    for proc in procs:
        f.write('{0[p_t]} {0[p_s]};\n'.format(proc_t(proc)).encode("utf-8"))
    f.write(br'''
static void load_procs(void)
{
''')
    for proc in procs:
        f.write('\t{0[p_s]} = ({0[p_t]}) get_proc("{0[p]}");\n'.format(proc_t(proc)).encode("utf-8"))
    f.write(b'}\n')
