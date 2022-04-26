import argparse, os, re
from subprocess import getoutput

def checkForDir(path):
	if os.path.isdir(path) == False:
		os.mkdir(path)

def alreadyAbstracted():
	present=True
	for l in range(args.level+1):
		if not os.path.exists('abs_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp'):
			print('Abstraction abs_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp not found. Please abstract with option -a')
			present = False
	return present
	
def alreadyAbstractedAndSolved():
	present = alreadyAbstracted()
	for l in range(args.level+1):
		if not os.path.exists('solv_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp'):
			print('Solved instance solv_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp not found. Please solve with option -s')
			present = False
	return present

def saveToFile(path, output, level):
	if 'ANSWER' in output:
		checkForDir(path)
		temp = open(path + INSTANCE_NAME + '_l' + str(level) + '.lp','w')
		temp.write(output.split("ANSWER",1)[1])
		temp.close()
	else:
		print('Level ' + str(level) + ' UNSAT!')

def getTimes():
	print("\nAbstraction times in s:")
	total_abs=0
	total_solv=0
	for l in range(args.level+1):
		datei = open('abs_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp','r')
		if (time := re.search('% Time           : (.*)s \(S', datei.read())) is not None:
			print('	Level ' + str(l) + ': ' + time.group(1))
			total_abs = total_abs + float(time.group(1))
	print('	Total  : ' + str(total_abs))

	print("\nSolving times in s:")
	total=0
	for l in range(args.level+1):
		datei = open('solv_inst/' + INSTANCE_NAME + '_l' + str(l) + '.lp','r')
		if (time := re.search('% Time           : (.*)s \(S', datei.read())) is not None:
			print('	Level ' + str(l) + ': ' + time.group(1))
			total_solv = total_solv + float(time.group(1))
	print('	Total  : ' + str(total_solv))
	print('\nComplete time  : ' + str(total_abs+total_solv))	

def abstract_clique(level):
	if level==0:
		output = getoutput('clingo abstraction/abs_0.lp ' + INSTANCE_PATH + ' --outf=1')
		saveToFile('abs_inst/', output, level)
	else:
		output = getoutput('clingo abstraction/abs_step.lp ' + INSTANCE_PATH + ' abs_inst/' + INSTANCE_NAME + '_l' + str(level-1) + '.lp --heuristic=Domain -c level=' + str(level) + '  --outf=1')
		saveToFile('abs_inst/', output, level)

def abstract_cross():
	output = getoutput('clingo abstraction/cross.lp ' + INSTANCE_PATH + ' -c level=1 --outf=1')
	saveToFile('abs_inst/', output, 1)

def solve(level):
	if level==0:
		output = getoutput('clingo abstraction/solving_0.lp solv_inst/' + INSTANCE_NAME + '_l' + str(level+1) + '.lp abs_inst/' + INSTANCE_NAME + '_l0.lp ' + INSTANCE_PATH + ' -c level=0 --outf=1 -c horizon=' + STEPS)
		saveToFile('solv_inst/', output, level)
	elif level==int(MAX_LVL):	
		output = getoutput('clingo abstraction/solving_step.lp abs_inst/' + INSTANCE_NAME + '_l' + MAX_LVL + '.lp ' + INSTANCE_PATH + ' -c level=' + MAX_LVL + ' --outf=1 -c horizon=' + STEPS)
		saveToFile('solv_inst/', output, level)	
	else:
		output = getoutput('clingo abstraction/solving_step.lp solv_inst/' + INSTANCE_NAME + '_l' + str(level+1) + '.lp abs_inst/' + INSTANCE_NAME + '_l' + str(level) + '.lp ' + INSTANCE_PATH + ' -c level=' + str(level) + ' --outf=1 -c horizon=' + STEPS)
		saveToFile('solv_inst/', output, level)
		
def visualize():
	os.system('clingo abs_inst/' + INSTANCE_NAME + '_l' + MAX_LVL + '.lp abstraction/clingraph.lp --outf=2 --heuristic=Domain -c level=' + MAX_LVL + ' | clingraph --json --select-model=1 --render --format=png --engine=neato')

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--instance",	help="Instance to be abstracted",	required=True)
parser.add_argument("-l", "--level",		help="Levels of abstraction to be created", type=int)
parser.add_argument("-t", "--timesteps",	help="Timesteps to find a plan in",         type=int)
parser.add_argument("-a", "--abstract",	help="Abstract instance",      	action='store_true')
parser.add_argument(      "--clique",		help="Use clique abstraction",	action='store_true')
parser.add_argument(      "--cross",		help="Use crossings abstraction",	action='store_true')
parser.add_argument("-s", "--solve",		help="Solve instance",         	action='store_true')
parser.add_argument("-v", "--visualize",	help="Visualize instance",     	action='store_true')
#parser.add_argument("-c", "--clean",		help="Clean up files afterwards",  	action='store_true')
parser.add_argument("-b", "--benchmark",	help="Analyze runtimes",       	action='store_true')


args = parser.parse_args()

if not args.solve and not args.abstract and not args.visualize and not args.benchmark:
	parser.error("Please specify at least one task to perform: --solve, --abstract, --visualize or --benchmark.")

if args.solve and args.timesteps is None:
	parser.error("--solve requires -t TIMESTEPS.")
	
re_result_instance = re.search('/(.*).lp', args.instance)
INSTANCE_NAME	= re_result_instance.group(1)
INSTANCE_PATH	= args.instance
MAX_LVL	= str(args.level)
STEPS		= str(args.timesteps)

if args.abstract and not args.clique and not args.cross:
	parser.error("Please specify abstraction type: --clique or --cross.")

if args.abstract and args.clique and args.cross:
	parser.error("Please specify only one abstraction type.")

if args.abstract and args.clique:
	if args.level is None:
		parser.error("--clique requires -l LEVELS.")
	else:
		for l in range(args.level+1):
			abstract_clique(l)

if args.abstract and args.cross:	
	abstract_cross()
		
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
