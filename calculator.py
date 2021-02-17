# desktop calculator app

import tkinter as tk

def op(s,a,b): # perform specified operation on a and b
	if s == '^':
		return a**b
	if s == u"\u00F7":
		return a/b
	if s == u"\u00D7":
		return a*b
	if s == '+':
		return a+b
	if s == '-':
		return a-b
		
# command functions for buttons

def enter(s):
	global entry
	if entry == 'ERROR':
		entry = ''
	entry += s
	lbl_display["text"] = entry

def clear():
	global entry
	entry = ""
	lbl_display["text"] = entry
	
def equal(string):
	global entry
	
	try:
		numbers = {'0','1','2','3','4','5','6','7','8','9','.'}
		ops = ['^',u"\u00F7",u"\u00D7",'+','-']
		# handle parentheses by recursion
		left = 0 # counts left parentheses
		right = 0 # counts right parentheses
		start = 0 # record part of string between parentheses
		i = 0
		while i < len(string):
			if string[i] == '(':
				if i > 0 and string[i-1] in numbers: # incorrect syntax
					entry = 'ERROR'
					lbl_display["text"] = entry
					return entry
				if left == 0:
					start = i+1
					left+=1
				else: left+=1
			if string[i] == ')':
				if i < len(string)-1 and string[i+1] in numbers: # incorrect syntax
					entry = 'ERROR'
					lbl_display["text"] = entry
					return entry
				right+=1
				if right == left: # found a pair of outer parentheses
					rec = equal(string[start:i])
					if rec == 'ERROR':
						entry = 'ERROR'
						lbl_display["text"] = entry
						return entry
					if i+1 < len(string):
						string = string[0:start-1]+rec+string[i+1:] 
					else:
						string = string[0:start-1]+rec+string[i+1:]
					left, right, start, i = 0,0,0,-1
			i+=1	
		
		parsed = [] # list holding string split into numbers and operations, all as strings
		temp = ''
		for c in string:
			if c in numbers:
				temp+=c
			elif c == '-' and temp == '':
				temp+=c
			else:
				parsed.append(temp)
				parsed.append(c)
				temp = ''
		if temp != '':
			parsed.append(temp)
		# apply order of operations: ^,/,*,+,-
		for s in ops:
			i = 0
			while i < len(parsed):
				if parsed[i] == s:
					a, b = float(parsed[i-1]),float(parsed[i+1])
					result = op(s,a,b)
					parsed[i-1] = str(result)
					parsed.pop(i+1)
					parsed.pop(i)
				else: i+=1
		entry = parsed[0]
		# check if integer, and eliminate decimal in that case
		if 'e' not in entry: # avoids cases in scientific notation
			if entry[-2:] == '.0':
				entry = entry[0:-2]
		lbl_display["text"] = entry
	except:
		entry = 'ERROR'
		lbl_display["text"] = entry
	return entry

window = tk.Tk()
window.title("Calculator")

frm_buttons = tk.Frame(master=window)
btn_0 = tk.Button(master=frm_buttons, text="0", command=lambda: enter('0'))
btn_1 = tk.Button(master=frm_buttons, text="1", command=lambda: enter('1'))
btn_2 = tk.Button(master=frm_buttons, text="2", command=lambda: enter('2'))
btn_3 = tk.Button(master=frm_buttons, text="3", command=lambda: enter('3'))
btn_4 = tk.Button(master=frm_buttons, text="4", command=lambda: enter('4'))
btn_5 = tk.Button(master=frm_buttons, text="5", command=lambda: enter('5'))
btn_6 = tk.Button(master=frm_buttons, text="6", command=lambda: enter('6'))
btn_7 = tk.Button(master=frm_buttons, text="7", command=lambda: enter('7'))
btn_8 = tk.Button(master=frm_buttons, text="8", command=lambda: enter('8'))
btn_9 = tk.Button(master=frm_buttons, text="9", command=lambda: enter('9'))
btn_point = tk.Button(master=frm_buttons, text=".", command=lambda: enter('.'))
btn_plus = tk.Button(master=frm_buttons, text="+", command=lambda: enter('+'))
btn_minus = tk.Button(master=frm_buttons, text="-", command=lambda: enter('-'))
btn_left = tk.Button(master=frm_buttons, text="(", command=lambda: enter('('))
btn_right = tk.Button(master=frm_buttons, text=")", command=lambda: enter(')'))
btn_exp = tk.Button(master=frm_buttons, text="^", command=lambda: enter('^'))
btn_times = tk.Button(master=frm_buttons, text=u"\u00D7", command=lambda: enter(u"\u00D7"))
btn_divide = tk.Button(master=frm_buttons, text=u"\u00F7", command=lambda: enter(u"\u00F7"))
btn_equal = tk.Button(master=frm_buttons,text="=", command=lambda: equal(entry))
btn_clear = tk.Button(master=frm_buttons,text="c", command=clear)

btn_0.grid(row=4, column=0)
btn_point.grid(row=4, column=1)
btn_1.grid(row=3, column=0)
btn_2.grid(row=3, column=1)
btn_3.grid(row=3, column=2)
btn_4.grid(row=2, column=0)
btn_5.grid(row=2, column=1)
btn_6.grid(row=2, column=2)
btn_7.grid(row=1, column=0)
btn_8.grid(row=1, column=1)
btn_9.grid(row=1, column=2)
btn_plus.grid(row=3, column=3)
btn_minus.grid(row=2, column=3)
btn_times.grid(row=1, column=3)
btn_divide.grid(row=0, column=3)
btn_equal.grid(row=4, column=3)
btn_clear.grid(row=4, column=2)
btn_left.grid(row=0, column=1)
btn_right.grid(row=0, column=2)
btn_exp.grid(row=0, column=0)

entry = ""
lbl_display = tk.Label(master=window, width=15, relief=tk.RIDGE, borderwidth=5, text=entry)


frm_buttons.grid(row=1, pady=10)
lbl_display.grid(row=0, padx=10)


window.mainloop()