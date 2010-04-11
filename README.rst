============================================
gl3w: Simple OpenGL 3/4 core profile loading
============================================

Introduction
------------

gl3w_ is the easiest way to get your hands on the functionality offered by
OpenGL 3/4 core profile specification.

It consists of a simple Python 2.6 script that downloads the Khronos_ supported
gl3.h_ header and generates gl3w.h and gl3w.c from it. The resulting files can
then be included and statically linked into your project.

Example
-------

Here is a simple example of using gl3w_ with glut::

    #include <stdio.h>
    #include <GL3/gl3w.h>
    #include <GL/glut.h>

    // ...

    int main(int argc, char **argv)
    {
            glutInit(&argc, argv);
            glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE);
            glutInitWindowSize(width, height);
            glutCreateWindow("cookie");

            glutReshapeFunc(reshape);
            glutDisplayFunc(display);
            glutKeyboardFunc(keyboard);
            glutSpecialFunc(special);
            glutMouseFunc(mouse);
            glutMotionFunc(motion);

            if (gl3wInit()) {
                    fprintf(stderr, "failed to initialize OpenGL\n");
                    return -1;
            }
            if (!gl3wIsSupported(3, 2)) {
                    fprintf(stderr, "OpenGL 3.2 not supported\n");
                    return -1;
            }
            printf("OpenGL %s, GLSL %s\n", glGetString(GL_VERSION),
                   glGetString(GL_SHADING_LANGUAGE_VERSION));

            // ...

            glutMainLoop();
            return 0;
    }

API Reference
-------------

The gl3w_ API consist of three functions:

``int gl3wInit(void)``

    Initializes the library. Should be called once after an OpenGL context has
    been created. Returns ``0`` when gl3w_ was initialized successfully,
    ``-1`` if there was an error.

``int gl3wIsSupported(int major, int minor)``

    Returns ``1`` when OpenGL core profile version *major.minor* is available,
    and ``0`` otherwise.

``void *gl3wGetProcAddress(const char *proc)``

    Returns the address of an OpenGL extension function. You probably won't need
    to use this function since gl3w_ loads all the functions defined in the
    OpenGL core profile. It's only exposed for completeness.

License
-------

gl3w_ is in the puclic domain.

Copyright
---------

2010 Slavomir Kaslev <slavomir.kaslev@gmail.com>

OpenGL_ is a registered trademark of SGI_.

.. _gl3w: http://github.com/skaslev/gl3w
.. _gl3.h: http://www.opengl.org/registry/api/gl3.h
.. _OpenGL: http://www.opengl.org/
.. _Khronos: http://www.khronos.org/
.. _SGI: http://www.sgi.com/
