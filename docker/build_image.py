#!/usr/bin/env python
import os

scripts_dir = os.path.dirname(os.path.abspath(__file__))
cwd = os.getcwd()

stages = [
	"docker build -t hopestarter-bin-deps --file=" + os.path.join(scripts_dir, "1.BinaryDeps") + " " + cwd,
	"docker build -t hopestarter-python-deps --file=" + os.path.join(scripts_dir, "2.PythonDeps") + " " + cwd,
	"docker build -t hopestarter-ansible --file=" + os.path.join(scripts_dir, "3.Ansible") + " " + cwd,
	"docker build -t hopestarter-server --file=" + os.path.join(scripts_dir, "4.ServerSetup") + " " + cwd
]

for i in xrange(len(stages)):
	print("------ Building stage " + str(i+1) + " of " + str(len(stages)))
	if os.system(stages[i]) != 0:
		print("ERROR: Build failed! Problem at stage " + str(i+1))
		break
