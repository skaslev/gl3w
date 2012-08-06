#!/usr/bin/env python
import re
import os
import urllib2

# Create directories
if not os.path.exists('include/GL'):
    os.makedirs('include/GL')
if not os.path.exists('src'):
    os.makedirs('src')

# Download glcorearb.h
if not os.path.exists('include/GL/glcorearb.h'):
    print 'Downloading glcorearb.h to include/GL...'
    web = urllib2.urlopen('http://www.opengl.org/registry/api/glcorearb.h')
    with open('include/GL/glcorearb.h', 'wb') as f:
        f.writelines(web.readlines())
else:
    print 'Reusing glcorearb.h from include/GL...'

# Parse function names from glcorearb.h
print 'Parsing glcorearb.h header...'
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
print 'Generating gl3w.h in include/GL...'
with open('include/GL/gl3w.h', 'wb') as f:
    f.write(r'''#ifndef __gl3w_h_
#define __gl3w_h_

#include <GL/glcorearb.h>

#ifndef __gl_h_
#define __gl_h_
#endif

#ifdef __cplusplus
extern "C" {
#endif

/* gl3w api */
int gl3wInit(void);
int gl3wIsSupported(int major, int minor);
void *gl3wGetProcAddress(const char *proc);

/* OpenGL functions */
''')
    for proc in procs:
        f.write('extern %(p_t)s %(p_s)s;\n' % proc_t(proc))
    f.write('\n')
    for proc in procs:
        f.write('#define %(p)s		%(p_s)s\n' % proc_t(proc))
    f.write(r'''
#ifdef __cplusplus
}
#endif

#endif
''')

# Generate gl3w.c
print 'Generating gl3w.c in src...'
with open('src/gl3w.c', 'wb') as f:
    f.write(r'''#include <GL/gl3w.h>

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

static void *get_proc(const char *proc)
{
	void *res;

	res = wglGetProcAddress(proc);
	if (!res)
		res = GetProcAddress(libgl, proc);
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

static void *get_proc(const char *proc)
{
	void *res;

	CFStringRef procname = CFStringCreateWithCString(kCFAllocatorDefault, proc,
		kCFStringEncodingASCII);
	res = CFBundleGetFunctionPointerForName(bundle, procname);
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

static void *get_proc(const char *proc)
{
	void *res;

	res = glXGetProcAddress((const GLubyte *) proc);
	if (!res)
		res = dlsym(libgl, proc);
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

void *gl3wGetProcAddress(const char *proc)
{
	return get_proc(proc);
}

''')
    for proc in procs:
        f.write('%(p_t)s %(p_s)s;\n' % proc_t(proc))
    f.write(r'''
static void load_procs(void)
{
''')
    for proc in procs:
        f.write('\t%(p_s)s = (%(p_t)s) get_proc("%(p)s");\n' % proc_t(proc))
    f.write('}\n')
