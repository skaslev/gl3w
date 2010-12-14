#include <stdio.h>
#include <stdlib.h>
#include <GL3/gl3w.h>
#include <GL/glut.h>

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
	glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH | GLUT_DOUBLE);
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
