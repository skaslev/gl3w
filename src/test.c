/*

    This file is part of gl3w, hosted at https://github.com/skaslev/gl3w

    This is free and unencumbered software released into the public domain.

    Anyone is free to copy, modify, publish, use, compile, sell, or
    distribute this software, either in source code form or as a compiled
    binary, for any purpose, commercial or non-commercial, and by any
    means.

    In jurisdictions that recognize copyright laws, the author or authors
    of this software dedicate any and all copyright interest in the
    software to the public domain. We make this dedication for the benefit
    of the public at large and to the detriment of our heirs and
    successors. We intend this dedication to be an overt act of
    relinquishment in perpetuity of all present and future rights to this
    software under copyright law.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
    EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
    MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
    IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
    OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
    OTHER DEALINGS IN THE SOFTWARE.

 */

#include <stdio.h>
#include <stdlib.h>
#include <GL/gl3w.h>
#ifdef __APPLE__
#include <GLUT/glut.h>
#else
#include <GL/glut.h>
#endif

static int width = 600, height = 600;

static float randf()
{
	return (float) rand() / ((float) RAND_MAX + 1);
}

static void display(void)
{
	glClearColor(randf(), randf(), randf(), 1.0f);
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	glutSwapBuffers();
	glutPostRedisplay();
}

static void reshape(int w, int h)
{
	width = w > 1 ? w : 1;
	height = h > 1 ? h : 1;
	glViewport(0, 0, width, height);
	glClearDepth(1.0);
	glClearColor(0.0f, 0.0f, 0.0f, 0.0f);
	glEnable(GL_DEPTH_TEST);
}

int main(int argc, char **argv)
{
	glutInit(&argc, argv);
	unsigned mode = GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE;
#ifdef __APPLE__
	mode |= GLUT_3_2_CORE_PROFILE;
#endif
	glutInitDisplayMode(mode);
	glutInitWindowSize(width, height);
	glutCreateWindow("cookie");

	glutReshapeFunc(reshape);
	glutDisplayFunc(display);

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

	glutMainLoop();
	return 0;
}
