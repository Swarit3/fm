#Import shit
import os
import curses
from math import ceil


#Define variables for screen and bottom text because of my incompetence to figure out how to work on a local variable across functions. Turns out, you can't.
scrnY, scrnX = 0, 0
bottomtxt = "Welcome"



def perline(stdscr, x: list, selnum: int, sp: int, subwin=True):
#Was supposed to be a simple function to print out list items linewise; now is the render function

	global bottomtxt
	scrnY, scrnX = stdscr.getmaxyx()

	stdscr.clear()

	for i in range(0,len(x)):
		if subwin == False:
			if os.path.isdir(x[i]):
				tc = 1
			elif os.path.isfile(x[i]):
				tc = 3
			else:
				tc = 5
		else:
			tc = 1

		if selnum == i:
			bc = 1
			if bottomtxt == "":
				if os.path.isdir(x[selnum]):
					try:
						bottomtxt = str(len(os.listdir(x[selnum]))) + " Items"
					except:
						bottomtxt = "Directory"
				elif os.path.isfile(x[selnum]):
					try:
						bottomtxt = str(os.path.getsize(x[i])/1048576)[0:4] + "MB"
					except:
						bottomtxt = "File"
				else:
					bottomtxt = "Unknown"
		else:
			bc = 0

		if (subwin == False and i+1-sp > 0 and i-sp < scrnY-3) or (subwin == True and i+1-sp > 0 and i-sp < scrnY-2):
			stdscr.addstr(i + 1 - sp + subwin, 0, '    '  + x[i][0:((scrnX - 7) if len(x[i]) > scrnX else len(x[i]))] + ('...' if len(x[i]) > scrnX else '') + ' '*ceil((scrnX-len(x[i]))-4), curses.color_pair(tc+bc))

	if subwin == False:
		stdscr.addstr(0, 0, ('...' if len(os.getcwd()) > scrnX else '') + os.getcwd()[len(os.getcwd()) - scrnX + 3 if len(os.getcwd()) > scrnX else 0:] + ' '*(scrnX-len(os.getcwd())), curses.color_pair(7))
		stdscr.addstr(scrnY-2, 0, ' '*ceil((scrnX-len(bottomtxt))/2) + bottomtxt + ' '*((scrnX-len(bottomtxt))//2), curses.color_pair(7))

	else:
		stdscr.addstr(1, 0, ' '*ceil((scrnX-len(bottomtxt))/2) + bottomtxt + ' '*(((scrnX-len(bottomtxt))//2)-1), curses.color_pair(7))
		stdscr.border()
		stdscr.refresh()



def lblinp(txt, ran = range(32, 127)):
	global scrnY, scrnX, bottomtxt
	popscr = curses.newwin(4, scrnX-2, ceil(scrnY-4)//2, ceil(scrnX//2))
	popscr.keypad(True)
	selnum = 0
	scrollpos = 0
	bottomtxt = txt
	out = str()
	while True:
		scrnY, scrnX = popscr.getmaxyx()
		kinp = popscr.getch()

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
			popscr.clear()
			perline(popscr, str(txt) + out, selnum, scrollpos)
			popscr.refresh()
		curses.napms(16)

	return out



def popup(opts: list, title=''):
	global scrnY, scrnX, bottomtxt
	popscr = curses.newwin(min(len(opts)+3, scrnX), min(len(title)+4, scrnY), ceil(scrnY-len(opts))//2, ceil(scrnX-len(title))//2)
	popscr.keypad(True)
	selnum = 0
	scrollpos = 0
	bottomtxt = title
	perline(popscr, opts, selnum, scrollpos)
	while True:
		kinp = popscr.getch()
		if kinp == curses.KEY_UP and selnum > 0:
			if selnum == scrollpos:
				scrollpos -= 1
			selnum -= 1
		elif kinp == curses.KEY_DOWN and selnum < len(opts)-1:
			if selnum == scrnY-4+scrollpos: #Don't ask why -4
				scrollpos += 1
			selnum += 1
		elif kinp in [curses.KEY_ENTER, 10, 13, 343]:
			break
		elif kinp in [curses.KEY_BACKSPACE, 8, 127]:
		    selnum = 0
		    break
		if kinp != -1:
			sizY, sizX = popscr.getmaxyx()
			perline(popscr, opts, selnum, scrollpos)
		curses.napms(16)
	bottomtxt = str()
	return selnum



class operation:

	def remove(obj):
		if not os.path.exists(obj):
			return

		if os.path.isdir(obj):
			if os.listdir(obj) != []:
				for subobj in os.listdir(obj):
					operation.remove(os.path.join(obj,subobj))
			os.rmdir(obj)
		elif os.path.isfile(obj):
			os.remove(obj)




def main(stdscr):
#Main program because curses is a bitch!
	#Init curses and import screen variables
	curses.curs_set(0)			#Hide Cursor
	stdscr.nodelay(True)
	curses.noecho()
	curses.cbreak()
	curses.start_color()		#enable color support
	stdscr.keypad(True)
	curses.use_default_colors()	#use default terminal colors. allows transparency
	global scrnY, scrnX, bottomtxt

	#Set variables
	scrollpos = 0
	selnum = 0
	scrnY, scrnX = stdscr.getmaxyx()
	#cdir = sorted(os.listdir(os.getcwd()))

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

		elif kinp == curses.KEY_UP and selnum > 0:
			if selnum == scrollpos:
				scrollpos -= 1
			selnum -= 1

		elif kinp == curses.KEY_DOWN and selnum < len(cdir)-1:
			if selnum == scrnY-4+scrollpos: #Don't ask why -4
				scrollpos += 1
			selnum += 1

		elif kinp == curses.KEY_HOME:
			selnum, scrollpos = 0, 0

		elif kinp == curses.KEY_END:
			selnum = len(cdir) - 1
			scrollpos = selnum - (scrnY-4) if selnum+2 > scrnY else 0


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
					#scrollpos = abs(scrnY - selnum)+6 if selnum+2 > scrnY else 0 #Adjust scroll position based on selector position and screen size
					scrollpos = selnum - (scrnY-4) if selnum+2 > scrnY else 0 #Adjust scroll position based on selector position and screen size
				except ValueError:
					bottomtxt = "Cannot go beyond " + os.getcwd()
				os.chdir('..')
		except (PermissionError, FileNotFoundError):
			bottomtxt = "Permission Denied!"
		except IndexError:
			#I have nothing to say
			pass


		if kinp == ord('t'):
			os.system(lblinp("$:"))
		
		elif kinp == ord('~'):
			os.chdir(os.path.expanduser('~'))

		elif kinp == ord(' '):
			opt = popup(['Rename', 'Delete'], "File Operations")
			if opt == 0:
				os.rename(cdir[selnum], lblinp("Rename"))
			elif opt == 1:
				if popup(['No', 'Yes'], "Are you sure you want to delete {}?".format(cdir[selnum])):
					operation.remove(cdir[selnum])



		#Debug loggr. for use with watch
		#open("/home/s/Documents/fm/log.txt", "w").write("scrnSIZE:"+ str(scrnY)+ str(scrnX)+ "\nselnum:"+ str(selnum)+ "\ncdir:"+ str(cdir)+ "\ncdir len:"+ str(len(cdir))+ "\nscrollpos:"+ str(scrollpos)+ "\nbottomtxt:"+ bottomtxt)


		if kinp != -1 or bottomtxt in ["Working directory inaccessible. Moved to {}".format(os.getcwd()), "Welcome", "hidden refresh"]:
			#Store items from current directory in a list and render them line-by-line.
			try:
				cdir = sorted(os.listdir(os.getcwd()))
				if cdir == []:
					bottomtxt = "Directory Empty"
				if selnum >= len(cdir):
					selnum = len(cdir) - 1
					bottomtxt = "hidden refresh"
					
			except FileNotFoundError: 
				while True:
					try:
						os.chdir("..")
						if os.path.exists(os.getcwd()):
							break
					except FileNotFoundError:
						continue
				bottomtxt = "Working directory inaccessible. Moved to {}".format(os.getcwd())
				continue

			#Draw.
			bottomtxt = '' if bottomtxt == "hidden refresh" else bottomtxt
			stdscr.move(0, 0)
			scrnY, scrnX = stdscr.getmaxyx()
			perline(stdscr, cdir, selnum, scrollpos, subwin = False)
			bottomtxt = ""
		curses.napms(16) #'wait for _' in milliseconds



#Actual execution ahead:
try:
	curses.wrapper(main)
except KeyboardInterrupt:
	print("Ctrl+C pressed.")
finally:
	print("Goodbye!")	

exit()



#To do:
#Fix: lplinp (its a mess. make it more rigid but easier to use)
