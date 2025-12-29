#Import shit
import os
import curses
from math import ceil

#Clear whatever mess there may be
if os.name == 'posix':
	os.system('clear')
elif os.name == 'nt':
	os.system('cls')

#Define variables for screen and bottom text because of my incompetence to figure out how to work on a local variable across functions.
scrnY, scrnX = 0, 0
bottomtxt = "Welcome"

def perline(stdscr, x, selnum, sp, dirs= False):
#Was supposed to be a simple function to print out list items linewise; now is the render function

	global bottomtxt
	scrnY, scrnX = stdscr.getmaxyx()

	stdscr.clear()

	for i in range(0,len(x)):
		if dirs == True:
			if os.path.isdir(x[i]) == True:
				tc = 1
			elif os.path.isfile(x[i]) == True:
				tc = 3
			else:
				tc = 5
		else:
			tc = 1

		if selnum == i:
			bc = 1
			if bottomtxt == "":
				if os.path.isdir(x[selnum]) == True:
					try:
						bottomtxt = str(len(os.listdir(x[selnum]))) + " Items"
					except:
						bottomtxt = "Directory"
				elif os.path.isfile(x[selnum]) == True:
					try:
						bottomtxt = str(os.path.getsize(x[i])/1048576)[0:4] + "MB"
					except:
						bottomtxt = "File"
				else:
					bottomtxt = "Unknown"
		else:
			bc = 0

		if (dirs == True and i+1-sp > 0 and i-sp < scrnY-3) or (dirs == False and i+1-sp > 0 and i-sp < scrnY-2):
			stdscr.addstr(i + 1 - sp, 0, '    '  + x[i][0:((scrnX - 7) if len(x[i]) > scrnX else len(x[i]))] + ('...' if len(x[i]) > scrnX else '') + ' '*ceil((scrnX-len(x[i]))-4), curses.color_pair(tc+bc))

	if dirs == True:
		try:
			stdscr.addstr(0, 0, ('...' if len(os.getcwd()) > scrnX else '') + os.getcwd()[len(os.getcwd()) - scrnX + 3 if len(os.getcwd()) > scrnX else 0:] + ' '*(scrnX-len(os.getcwd())), curses.color_pair(7))
		except FileNotFoundError: 
			#Hereonout, tc and bc are reused as... something. idk i forgor :skullemoji: lol 
			#oh wait, it's parent directories. and grandparent directories.
			tc, bc = 0, '..'
			while True:
				try:
					bc += "/.."*tc
					os.chdir(bc)
					break
				except FileNotFoundError:
					tc += 1
				if tc > 50:
					os.system('cd ~')
				bottomtxt = "Working directory inaccessible. Moved to " + os.getcwd()
		stdscr.addstr(scrnY-2, 0, ' '*ceil((scrnX-len(bottomtxt))/2) + bottomtxt + ' '*((scrnX-len(bottomtxt))//2), curses.color_pair(7))

	else:
		stdscr.addstr(0, 0, ' '*ceil((scrnX-len(bottomtxt))/2) + bottomtxt + ' '*((scrnX-len(bottomtxt))//2), curses.color_pair(7))
		stdscr.refresh()



def lblinp(stdscr, posY, posX, txt, ran = range(32, 127), cset = 7, rlist = True):
	global scrnY, scrnX
	out = str()
	stdscr.addstr(posY, posX, txt + ' '*(scrnX-len(txt)), curses.color_pair(cset))

	while True:
		scrnY, scrnX = stdscr.getmaxyx()
		kinp = stdscr.getch()

		if kinp in [curses.KEY_ENTER, 10, 13, 343]:
			break

		elif kinp in [curses.KEY_BACKSPACE, 127, 8] and len(out) > 0:
			out = out[:len(out)-1]

		elif kinp in ran:
			try:
				out = out + chr(kinp)
			except TypeError:
				pass

		if kinp != -1:
			stdscr.clear()
			if rlist == True:
				perline(stdscr, sorted(os.listdir('.')), -1, 0, dirs = True)
			stdscr.addstr(posY, posX, txt + out + '_' + ' '*(scrnX-len(txt+out)-1) , curses.color_pair(cset))
			stdscr.refresh()
		curses.napms(16)

	return out



def popup(opts=list(), title=''):
	global scrnY, scrnX, bottomtxt
	popscr = curses.newwin(len(opts)+2, len(title)+2, ceil(scrnY-len(opts))//2, ceil(scrnX-len(title))//2)
	selnum = 0
	scrollpos = 0
	bottomtxt = title
	perline(popscr, opts, selnum, scrollpos)
	while True:
		kinp = popscr.getch()
		#bottomtxt=str(kinp)
		if kinp in [curses.KEY_UP, 65] and selnum > 0:
			if selnum == scrollpos:
				scrollpos -= 1
			selnum -= 1
		elif kinp in [curses.KEY_DOWN, 66] and selnum < len(opts)-1:
			if selnum == scrnY-4+scrollpos: #Don't ask why -4
				scrollpos += 1
			selnum += 1
		elif kinp in [curses.KEY_ENTER, 10, 13, 343]:
			break
		elif kinp in [curses.KEY_BACKSPACE, 8, 127]:
		    selnum = 0
		    break
		elif kinp != -1:
			sizY, sizX = popscr.getmaxyx()
			perline(popscr, opts, selnum, scrollpos)
		curses.napms(16)
	bottomtxt = str()
	return selnum




def main(stdscr):
#Main program because curses is a bitch!
	#Init curses and import screen variables
	curses.curs_set(0)
	stdscr.nodelay(True)
	curses.noecho()
	curses.cbreak()
	curses.start_color()
	stdscr.keypad(True)
	curses.use_default_colors()
	global scrnY, scrnX, bottomtxt

	#Set variables
	scrollpos = 0
	selnum = 0
	scrnY, scrnX = stdscr.getmaxyx()
	f_ref = 1

	#Define color pairs
	curses.init_pair(1, curses.COLOR_GREEN, -1)
	curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_WHITE)
	curses.init_pair(3, curses.COLOR_BLUE, -1)
	curses.init_pair(4, curses.COLOR_BLUE, curses.COLOR_WHITE)
	curses.init_pair(7, curses.COLOR_WHITE, curses.COLOR_BLUE)
	curses.init_pair(8, curses.COLOR_WHITE, curses.COLOR_CYAN)
	curses.init_pair(5, curses.COLOR_RED, -1)
	curses.init_pair(6, curses.COLOR_RED, curses.COLOR_WHITE)


	while True:
	#Core loop

		#Key input system; To-do: Move this to a seperate function.
		kinp = stdscr.getch()
		if kinp == ord('q') and popup(['No', 'Yes'], "Are you sure you want to quit?"):
			break

		if kinp == curses.KEY_UP and selnum > 0:
			if selnum == scrollpos:
				scrollpos -= 1
			selnum -= 1

		if kinp == curses.KEY_DOWN and selnum < len(cdir)-1:
			if selnum == scrnY-4+scrollpos: #Don't ask why -4
				scrollpos += 1
			selnum += 1

		try:
		#Wrap navigating Directories in 'try' because you may not be allowed in some places. More likely on Posix based systems.
			if kinp in [curses.KEY_ENTER, 10, 13, 343] and selnum <= len(cdir) and os.path.isdir(cdir[selnum]):
				os.chdir(cdir[selnum])
				scrollpos = 0
				selnum = 0

			elif kinp in [curses.KEY_BACKSPACE, 127, 8] and os.path.exists(".."):
				try:
					#The following used to be the most CPU intensive line once. Then I learnt about inline conditions.
					selnum = sorted(os.listdir('..')).index(os.path.basename(os.getcwd()))
					scrollpos = abs(scrnY - selnum)+6 if selnum+2 > scrnY else 0 #Adjust scroll position based on selector position and screen size
				except ValueError:
					bottomtxt = "Cannot go beyond " + os.getcwd()
				os.chdir('..')
		except (PermissionError, FileNotFoundError):
			bottomtxt = "Permission Denied!"
		except IndexError:
			#I have nothing to say
			pass


		if kinp == ord('t'):
			os.system(lblinp(stdscr, scrnY-2, 0, "$:"))
		
		if kinp == ord('~'):
			os.chdir(os.path.expanduser('~'))

		if kinp == ord(' '):
			opt = popup(['Rename', 'Delete'], "File Operations")
			if opt == '0':
				lblinp(stdscr, )


		#Store items from current directory in a list and render them line-by-line.
		try:
			cdir = sorted(os.listdir('.'))
			if cdir == []:
				bottomtxt = "Directory Empty"
		except:
			cdir = []
			bottomtxt = "Directory Inaccessible"


		if kinp != -1 or f_ref > 0:
			stdscr.move(0, 0)
			scrnY, scrnX = stdscr.getmaxyx()
			perline(stdscr, cdir, selnum, scrollpos, dirs = True)
			if f_ref != 0:
				f_ref -= 1
			bottomtxt = ""
		curses.napms(16) #'wait for _' in milliseconds



#Actual execution ahead:
try:
	curses.wrapper(main)
except KeyboardInterrupt:
	print("Ctrl+C pressed.")
finally:
	if os.name == 'posix':
		os.system('clear')
	elif os.name == 'nt':
		os.system('cls')
	print("Goodbye!")

exit()



'''To do:
Move input logic to its own function. Update: No. Not doing that. Modularity will fuck up adaptability.
Add more controls (force refresh 'r'), (force 60Frame cycle 'R'), (move to end 'N'), (move to beginning 'J')
Fix: lplinp (its a mess. make it more rigid but easier to use)'''
