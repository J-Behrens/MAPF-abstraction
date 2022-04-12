import argparse, os, re
from subprocess import getoutput

def alreadyAbstracted():
	present=True
	for l in range(args.level+1):
		if not os.path.exists('abs_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp'):
			print('Abstraction abs_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp not found. Please abstract with option -a')
			present = False
	return present
	
def alreadyAbstractedAndSolved():
	alreadyAbstracted()
	for l in range(args.level+1):
		if not os.path.exists('solv_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp'):
			print('Abstraction solv_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp not found. Please solve with option -s')
			present = False
	return present

def saveToFile(path, output, level):
	temp = open(path + INSTANCE_NAME + '_l' + str(level) + '.lp','w')
	temp.write(output.split("ANSWER",1)[1])
	temp.close()


	
def getTimes():
	# für abs:
	for l in range(args.level+1):
	# Dateien öffnen
		datei = open('abs_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp','r')
		print(datei.read())
	# Zeiten filtern
	# Zeiten addieren
	# Zeiten abspeichern (als csv)
	
	# für solv:
	

def abstract(level):
	if level==0:
		output = getoutput('clingo abstraction/abs_0.lp ' + INSTANCE_PATH + ' --outf=1')
		saveToFile('abs_inst/', output, level)

	else:
		output = getoutput('clingo abstraction/abs_1.lp ' + INSTANCE_PATH + ' abs_inst/' + INSTANCE_NAME + '_l' + str(level-1) + '.lp -c level=' + str(level) + ' --heuristic=Domain --outf=1')
		saveToFile('abs_inst/', output, level)


def solve(level):
	if level==0:
		output = getoutput('clingo abstraction/solving_0.lp solv_inst/' + INSTANCE_NAME + '_l' + str(level+1) + '.lp abs_inst/' + INSTANCE_NAME + '_l0.lp ' + INSTANCE_PATH + ' -c level=0 --outf=1 -c horizon=' + TIMESTEPS)
		saveToFile('solv_inst/', output, level)
	elif level==int(MAX_LEVEL):	
		output = getoutput('clingo abstraction/solving_step.lp abs_inst/' + INSTANCE_NAME + '_l' + MAX_LEVEL + '.lp ' + INSTANCE_PATH + ' -c level=' + MAX_LEVEL + ' --outf=1 -c horizon=' + TIMESTEPS)
		saveToFile('solv_inst/', output, level)
		
	else:
		output = getoutput('clingo abstraction/solving_step.lp solv_inst/' + INSTANCE_NAME + '_l' + str(level+1) + '.lp abs_inst/' + INSTANCE_NAME + '_l' + str(level) + '.lp ' + INSTANCE_PATH + ' -c level=' + str(level) + ' --outf=1 -c horizon=' + TIMESTEPS)
		saveToFile('solv_inst/', output, level)
		
def visualize():
	os.system('clingo abs_inst/' + INSTANCE_NAME + '_l' + MAX_LEVEL + '.lp abstraction/clingraph.lp --outf=2 --heuristic=Domain -c level=' + MAX_LEVEL + ' | clingraph --json --select-model=1 --render --format=png --engine=neato')


parser = argparse.ArgumentParser()
parser.add_argument("-l", "--level",		help="Levels of abstraction to be created", type=int, required=True)
parser.add_argument("-t", "--timesteps",	help="Timesteps to find a plan in",         type=int)
parser.add_argument("-i", "--instance",	help="Instance to be abstracted",                     required=True)

parser.add_argument("-s", "--solve",		help="Solve instance",         action='store_true')
parser.add_argument("-a", "--abstract",	help="Abstract instance",      action='store_true')
parser.add_argument("-v", "--visualize",	help="Visualize instance",     action='store_true')
parser.add_argument("-c", "--clean",		help="Clean up output files",  action='store_true')
parser.add_argument("-b", "--benchmark",	help="Analyze runtimes",       action='store_true')
#parser.add_argument(      "--clique",		help="Use clique abstraction", action='store_true')
#parser.add_argument(      "--cross",		help="Use crossings abstraction", action='store_true')

args = parser.parse_args()

if args.solve and args.timesteps is None:
	parser.error("--solve requires -t TIMESTEPS.")
	
re_result_instance = re.search('/(.*).lp', args.instance)
INSTANCE_NAME	= re_result_instance.group(1)
INSTANCE_PATH	= args.instance
MAX_LEVEL	= str(args.level)
TIMESTEPS	= str(args.timesteps)
	
if args.abstract:
	for l in range(args.level+1):
		abstract(l)
		
if args.solve:
	if alreadyAbstracted():
		for l in range(args.level+1):
			solve(args.level - l)
		
if args.visualize:
	if alreadyAbstracted():
		visualize()
		
if args.benchmark:
	if alreadyAbstractedAndSolved():
		getTimes()
