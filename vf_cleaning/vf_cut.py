import subprocess
pipe = subprocess.Popen(['cut','-f','1,22,26-29,76-84,86','<VF_NAME>.txt'],stdout=subprocess.PIPE)
with open('<VF_NAME>.cut', 'w') as f:
	f.writelines(pipe.stdout)
