import tkinter as tk
import math
import re
import sqlite3
import random
import numpy as np
import matplotlib.pyplot as plt
import os

class Calculator:
  def __init__(self, master):
    #Create the main frame for the calculator
    self.frame = tk.Frame(master)
    self.frame.pack(expand=True, fill='both')

    #Create the display for the calculator
    #Set the font and the size of the frame
    self.display = tk.Text(self.frame, font=("Helvetica", 24), width=30, height=10)
    #Set the position of the box, relative to the window
    self.display.grid(row=0, column=0, rowspan=25, sticky='nsew')
    #Connects the text box to key press function
    self.display.bind("<Key>", self.keyPress)
    #Allows the key press function to work by assigning it to the text box
    self.display.focus_set()

    #Call the function to create the buttons for the calculator
    self.createButtons()

  def createButtons(self):
    #Create the button frame
    buttonFrame = tk.Frame(self.frame)
    buttonFrame.grid(row=0, column=1, rowspan=2, sticky='nsew')

    #Create the buttons
    buttonList = [
            ["AC", "÷", "×", "-", "x²", "x³", "xʸ", "√", "×10^x", "1/x", "A"],
            ["7", "8", "9", "+", "MOD", "DIV", "RAND", "log", "ln", "e", "B"], 
            ["4", "5", "6", "π", "sinr", "cosr", "tanr", "sind", "cosd", "tand", "C"],
            ["1", "2", "3", "!", "sinir", "cosir", "tanir", "sinid", "cosid", "tanid", "X"],
            ["0", ".", "=", ",", "(", ")", "Quad", "SUVAT", "Graph", "STORE", "Y"]
        ]
    #Go along x axis, creating each button
    for i, row in enumerate(buttonList):
      #Go along y axis, creating each button
        for j, text in enumerate(row):
            button = tk.Button(buttonFrame, text=text, font=("Courier", 18), width=5, height=2, command=lambda text=text: self.buttonPress(text))
            #Set the inverse trig functions to be coloured red
            if text in ["sinir", "cosir", "tanir", "sinid", "cosid", "tanid"]:
              button.config(bg="red")
            #Set the trig functions to be coloured orange
            if text in ["sinr", "cosr", "tanr", "sind", "cosd", "tand"]:
              button.config(bg="orange")
            #Set the logarithmic functions to be coloured blue
            if text in ["log", "ln", "e"]:
              button.config(bg="blue")
            #Set these to be coloured brown
            if text in ["MOD", "DIV", "RAND"]:
              button.config(bg= "brown")
            #Set the basic arithmetic functions to be coloured pink
            if text in ["÷", "×", "-", "π", ",", "=", "!", "+", "(", ")"]:
              button.config(bg="#F590FC")
            #Set the unique functions to be coloured yellow
            if text in ["Quad", "SUVAT", "Graph", "STORE"]:
              button.config(bg="yellow")
            #Set these functions to be coloured green
            if text in ["x²", "x³", "xʸ", "√",  "×10^x", "1/x"]:
                button.config(bg="green")
            if text in ["A", "B", "C", "X", "Y"]:
                button.config(bg="#C270DD")
            #Set number buttons to be coloured in a lighter shade of purple
            elif text in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."]:
              button.config(bg="#F600FF")
            button.grid(row=i, column=j, padx=2, pady=2)

  def keyPress(self, event):
    try:
      #Handle the equal key and the enter key
      if event.char in ["=", "\r"]:
        #Evaluate the input in the text box and display the result
        #Get the current line number
        lineNumber = int(self.display.index("insert").split(".")[0])
        #Get the text of the current line
        lineText = self.display.get("{}.0".format(lineNumber), "{}.end".format(lineNumber))

        #Replace these characters for calculation 
        if "²" in lineText or "³" in lineText or "^" in lineText:
          lineText = self.replacePowers(lineText)
        if "√" in lineText:
          lineText = self.replaceRoots(lineText)
        if "log" in lineText or "ln" in lineText or "e" in lineText:
          lineText = self.replaceLogs(lineText)
        if "sinr" in lineText or "cosr" in lineText or "tanr" in lineText:
          lineText = self.replaceTrigRadians(lineText)
        if "sind" in lineText or "cosd" in lineText or "tand" in lineText:
          lineText = self.replaceTrigDegrees(lineText)
        if "sinid" in lineText or "cosid" in lineText or "tanid" in lineText:
          lineText = self.replaceInverseDegrees(lineText)
        if "sinir" in lineText or "cosir" in lineText or "tanir" in lineText:
          lineText = self.replaceInverseRadians(lineText)
        if "!" in lineText:
          lineText = self.replaceFactorial(lineText)
        if "rand(" in lineText:
          lineText = self.doRandom(lineText)
        if "A" in lineText:
            lineText= self.replaceA(lineText)
        if "B" in lineText:
            lineText= self.replaceB(lineText)
        if "C" in lineText:
            lineText= self.replaceC(lineText)
        if "X" in lineText:
            lineText= self.replaceX(lineText)
        if "Y" in lineText:
            lineText= self.replaceY(lineText)

        #Put asterisk in front of any brackets to allow for calculations
        lineText = self.addAsterisk(lineText) 
                
        #Remove leading zero
        lineText = self.removeLeadingZero(lineText)
                          
         #Evaluate the line text
        result = eval(lineText)
        #Format result to 10 decimal places
        result = "{:.10f}".format(result)
        #Display the answer followed by a blank line
        self.display.insert("end", "\n")
        self.display.insert("end", float(result))
        #Go to a new line
        self.newCalc()
      #If user divides by zero or other zero error
    except ZeroDivisionError:
        self.display.insert("end","\nMath Error\n")
    except ValueError:
        self.display.insert("end","\nMath Error\n")
      #User inputs wrong syntax
    except SyntaxError:
        self.display.insert("end","\nSyntax Error\n")

  def buttonPress(self, value):
    try:
      if value == "=":
        #If equals button is pressed, evaluate the input in the text box and display the result
        #Get the current line number
        lineNumber = int(self.display.index("insert").split(".")[0])
        #Get the text of the current line
        lineText = self.display.get("{}.0".format(lineNumber), "{}.end".format(lineNumber))
        #Replace the following for calculation
        if "²" in lineText or "³" in lineText  or "^" in lineText:
          lineText = self.replacePowers(lineText)
        if "√" in lineText:
          lineText = self.replaceRoots(lineText)
        if "log" in lineText or "ln" in lineText or "e" in lineText:
          lineText = self.replaceLogs(lineText)
        if "sinr" in lineText or "cosr" in lineText or "tanr" in lineText:
          lineText = self.replaceTrigRadians(lineText)
        if "sind" in lineText or "cosd" in lineText or "tand" in lineText:
          lineText = self.replaceTrigDegrees(lineText)
        if "sinid" in lineText or "cosid" in lineText or "tanid" in lineText:
          lineText = self.replaceInverseDegrees(lineText)
        if "sinir" in lineText or "cosir" in lineText or "tanir" in lineText:
          lineText = self.replaceInverseRadians(lineText)
        if "!" in lineText:
          lineText = self.replaceFactorial(lineText)
        if "π" in lineText:
          lineText = self.replacePi(lineText)
        if "A" in lineText:
            lineText= self.replaceA(lineText)
        if "B" in lineText:
            lineText= self.replaceB(lineText)
        if "C" in lineText:
            lineText= self.replaceC(lineText)
        if "X" in lineText:
            lineText= self.replaceX(lineText)
        if "Y" in lineText:
            lineText= self.replaceY(lineText)

        #Put asterisk in front of any brackets to allow for calculations
        lineText = self.addAsterisk(lineText) 
        #Remove leading zero
        lineText = self.removeLeadingZero(lineText)
                        
         #Evaluate the line text
        result = eval(lineText) 
        #Format to 10 decimal places
        result = "{:.10f}".format(result)
        #Display the answer followed by a blank line
        self.newCalc()
        self.display.insert("end", float(result))
        self.newCalc()
        self.newCalc()
      #If user divides by zero or other zero error
    except ZeroDivisionError:
      self.display.insert("end","\nMath Error\n")
    except ValueError:
        self.display.insert("end","\nMath Error\n")
      #If user inputs wrong syntax
    except SyntaxError:
      self.display.insert("end","\nSyntax Error\n")

    #Handle clear keys
    #If AC button is pressed, clear everything
    if value == "AC":
        self.display.delete("1.0", "end")
        
    #Handle the divide and multiply buttons
    if value == "×":
      self.display.insert("insert", "*")
    elif value == "÷":
      self.display.insert("insert","/")

    #Handle these buttons
    elif value in ["x²", "x³", "xʸ", "√", "()"]: 
        if value == "x²":
          self.display.insert("insert", "()²")
        elif value == "x³":
          self.display.insert("insert", "()³")
        elif value == "xʸ":
          self.display.insert("insert", "**")
        elif value == "√":
          self.display.insert("insert", "√(")
        elif value == "()":
          self.display.insert("insert", "()")

    #Handle these buttons
    elif value in ["×10^x", "1/x"]:
      if value == "×10^x":
        self.display.insert("insert", "*(10^")
      if value == "1/x":
        self.display.insert("insert", "(1/")

    #Handle these log buttons
    elif value in ["ln", "log", "e", "π"]:
        if value == "log":
            self.display.insert("insert", "log(")
        if value == "ln":
            self.display.insert("insert", "ln(")
        if value == "π":
            self.display.insert("insert", "π")
        if value == "e":
            self.display.insert("insert", "e")

    #Handle the trig functions
    elif value in ["sinr", "cosr", "tanr"]:
      if value == "sinr":
        self.display.insert("insert", "sinr(")
      if value == "cosr":
        self.display.insert("insert", "cosr(")
      if value == "tanr":
        self.display.insert("insert", "tanr(")
    elif value in ["sind", "cosd", "tand"]:
      if value == "sind":
        self.display.insert("insert", "sind(")
      if value == "cosd":
        self.display.insert("insert", "cosd(")
      if value == "tand":
        self.display.insert("insert", "tand(")

    #Handle the inverse trig functions
    elif value in ["sinir", "cosir", "tanir"]:
      if value == "sinir":
        self.display.insert("insert", "sinir(")
      if value == "cosir":
        self.display.insert("insert", "cosir(")
      if value == "tanir":
        self.display.insert("insert", "tanir(")
    elif value in ["sinid", "cosid", "tanid"]:
      if value == "sinid":
        self.display.insert("insert", "sinid(")
      if value == "cosid":
        self.display.insert("insert", "cosid(")
      if value == "tanid":
        self.display.insert("insert", "tanid(")

    #Handle the modulus, integer division, and rand functions
    elif value in ["MOD", "DIV", "RAND"]:
      if value == "MOD":
        self.display.insert("insert", "%")
      if value == "DIV":
        self.display.insert("insert", "//")
      if value == "RAND":
        self.display.insert("insert", "rand( , )")

    #Handle the unique functions
    elif value == "SUVAT":
      self.openSUVATWindow()
    elif value == "Quad":
      self.openQuadWindow()
    elif value == "STORE":
      self.store()
    elif value == "Graph":
      self.graphing()

    elif value == "A" or value == "B" or value == "C" or value == "X" or value == "Y":
      self.display.insert("insert", value)
      
    #Handle all other buttons, includes number buttons
    else:
      if value != "=" and value != "AC":
        self.display.insert("insert", value)

  #Clear the display
  def clearDisplay(self, event):
      self.display.delete("1.0", "end")

  #Add a new line for new calculations
  def newCalc(self):
    self.display.insert("end", "\n")

  def addAsterisk(self, string):
      result = ""
      i = 0
      #Look through each character in the input string
      while i < len(string):
          #If the character is an opening bracket and it is the first character in the string, add it to the result string
          if string[i] == '(' and i == 0:
              result += string[i]
          #If the current character is an opening bracket and the previous character is a digit or closing bracket, add an asterisk
          elif string[i] == '('  and (string[i - 1].isdigit() or string[i - 1] == ")"):
              result +='*'+string[i]
          #Otheriwse, add current character to the result string
          else:
              result += string[i]
          #Increment i variable to move onto the next character
          i += 1
      return result

  def replacePowers(self, string):
    while "²" in string or "³" in string or "^" in string:
      #Replaces ² with **2 so it can be evaluated
      string = re.sub(r'\)\²', ')**2', string)
      #Replaces ³ with **3 so it can be evaluated
      string = re.sub(r'\)\³', ')**3', string)
      #Replaces ^ with ** so it can be evaluated
      string = re.sub(r'\^', '**', string)
    return string
    
  def replaceRoots(self, string):
    while "√" in string:
      #Place a **0.5 at the end of the bracket (equivalent to square root)
      string= re.sub(r'\)', ')**0.5', string)
      #Remove the square root symbol
      string = string.replace("√", "")
    return string

  def replaceLogs(self, string):
    while "log" in string:
      #Indexes to locate the expression which needs to be log-ed
      start = string.index("log(")
      end = string.index(")", start)
      bracketExpression = string[start+4:end]
      #Performs the log (base 10) function on the expression contained in the brackets
      result = math.log(eval(bracketExpression), 10)
      #Replaces the old expression including the "log" with the answer
      string = string[:start] + str(result) + string[end+1:]
    while "ln" in string:
      #Indexes to locate the expression which needs to be ln-ed
      start = string.index("ln(")
      end = string.index(")", start)
      bracketExpression = string[start+3:end]
      #Performs the log (base e) function on the expression contained in the brackets
      result = math.log(eval(bracketExpression), math.e)
      #Replaces the old expression including "ln" with the answer
      string = string[:start] + str(result) + string[end+1:]
    #Remove all appearances of these characters
    string = string.replace("e", "math.e")
    string = string.replace("ln", "")
    string = string.replace("log", "")
    return string

  def replaceTrigRadians(self, string):
    while "sinr(" in string:
      #Indexes to locate the expression which needs to be sin-ed
        start = string.index("sinr(")
        end = string.index(")", start)
        bracketExpression = string[start+5:end]
        #Performs the sin (radians) function
        result = math.sin(eval(bracketExpression))
        #Replaces the old expression including "sinr(" with the answer
        string = string[:start] + str(result) + string[end+1:]
    while "cosr(" in string:
      #Indexes to locate the expression which needs to be cos-ed
        start = string.index("cosr(")
        end = string.index(")", start)
        bracketExpression = string[start+5:end]
        #Performs the cos (radians) function
        result = math.cos(eval(bracketExpression))
        #Replaces the old expression including "sinr(" with the answer
        string = string[:start] + str(result) + string[end+1:]
    while "tanr(" in string:
      #Indexes to locate the expression which needs to be tan-ed
        start = string.index("tanr(")
        end = string.index(")", start)
        bracketExpression = string[start+5:end]
        #Performs the tan (radians) function
        result = math.tan(eval(bracketExpression))
        #Replaces the old expression including "sinr(" with the answer
        string = string[:start] + str(result) + string[end+1:]
    #if it is a multiple of pi/2 then show Math Error
    if result >= 100000:
      self.display.insert("end", "\nMath Error\n")
    else:
      #Remove all appearances of these characters
      string = string.replace("sinr", "")
      string = string.replace("cosr", "")
      string = string.replace("tanr", "")
      return string
      
  def replaceTrigDegrees(self, string):
    while "sind(" in string:
        #Indexes to locate the expression which needs to be sin-ed
        start = string.index("sind(")
        end = string.index(")", start)
        bracketExpression = string[start+5:end]
        #Performs the sin (degrees) function
        radians = math.radians(eval(bracketExpression))
        result = math.sin(radians)
        #Replaces the old expression including "sind(" with the answer
        string = string[:start] + str(result) + string[end+1:]
    while "cosd(" in string:
        #Indexes to locate the expression which needs to be sin-ed
        start = string.index("cosd(")
        end = string.index(")", start)
        bracketExpression = string[start+5:end]
        #Performs the cos (degrees) function
        radians = math.radians(eval(bracketExpression))
        result = math.cos(radians)
        #Replaces the old expression including "cosd(" with the answer
        string = string[:start] + str(result) + string[end+1:]
    while "tand(" in string:
        #Indexes to locate the expression which needs to be sin-ed
        start = string.index("tand(")
        end = string.index(")", start)
        bracketExpression = string[start+5:end]
        #Performs the tan (degrees) function
        radians = math.radians(eval(bracketExpression))
        result = math.tan(radians)
        #Replaces the old expression including "tan(" with the answer
        string = string[:start] + str(result) + string[end+1:]
    #if it is a multiple of 90 then show Math Error
    if result >= 100000:
      self.display.insert("end", "\nMath Error\n")
    else:
      #Remove all appearances of these characters
      string = string.replace("sind", "")
      string = string.replace("cosd", "")
      string = string.replace("tand", "")
      return string

  def replaceInverseDegrees(self, string):
      while "sinid" in string:
            #Indexes to locate the expression which needs to be sin-ed
            start = string.index("sinid(")
            end = string.index(")", start)
            bracketExpression = string[start+6:end]
            #Performs the inverse sin (degrees) function
            result = str(math.degrees(math.asin(float(bracketExpression))))
            #Concatenate with the answer
            string = string[:start] + str(result) + string[end+1:]
      while "cosid" in string:
            #Indexes to locate the expression which needs to be cos-ed
            start = string.index("cosid(")
            end = string.index(")", start)
            bracketExpression = string[start+6:end]
            #Performs the inverse cos (degrees) function
            result = str(math.degrees(math.acos(float(bracketExpression))))
            #Concatenate with the answer
            string = string[:start] + str(result) + string[end+1:]
      while "tanid" in string:
            #Indexes to locate the expression which needs to be tan-ed
            start = string.index("tanid(")
            end = string.index(")", start)
            bracketExpression = string[start+6:end]
            #Performs the inverse tan (degrees) function
            result = str(math.degrees(math.atan(float(bracketExpression))))
            #Concatenate with the answer
            string = string[:start] + str(result) + string[end+1:]
      #Remove all appearances of these characters
      string = string.replace("sinid", "")
      string = string.replace("cosid", "")
      string = string.replace("tanid", "")
      return string
    
  def replaceInverseRadians(self, string):
      while "sinir" in string:
            #Indexes to locate the expression which needs to be sin-ed
            start = string.index("sinir(")
            end = string.index(")", start)
            bracketExpression = string[start+6:end]
            #Performs the inverse sin (radians) function
            result = str(math.asin(float(bracketExpression)))
            #Concatenate with the answer
            string = string[:start] + str(result) + string[end+1:]
      while "cosir" in string:
            #Indexes to locate the expression which needs to be cos-ed
            start = string.find("cosir(")
            end = string.find(")", start)
            bracketExpression = string[start+6:end]
            #Performs the inverse cos (radians) function
            result = str(math.acos(float(bracketExpression)))
            #Concatenate with the answer
            string = string[:start] + str(result) + string[end+1:]
      while "tanir" in string:
            #Indexes to locate the expression which needs to be tan-ed
            start = string.find("tanir(")
            end = string.find(")", start)
            bracketExpression = string[start+6:end]
            #Performs the inverse tan (radians) function
            result = str(math.atan(float(bracketExpression)))
            #Concatenate with the answer
            string = string[:start] + str(result) + string[end+1:]
      #Remove all appearances of these characters
      string = string.replace("sinir", "")
      string = string.replace("cosir", "")
      string = string.replace("tanir", "")
      return string

  def replaceFactorial(self, string):
    #Find index location of the factorial
    start = string.find("!")
    while start != -1:
        #Initialise the variable to hold the total
        number = ""
        i = start-1
        while i >= 0 and string[i].isdigit():
            number = string[i] + number
            #Decrement 
            i -= 1
        number = int(number)
        factorial = math.factorial(number)
        #Concatenate with the answer
        string = string[:i+1] + str(factorial) + string[start+1:]
        start = string.find("!",start+len(str(factorial)))
    return string

  def replacePi(self, string):
    while "π" in string:
      string = string.replace("π", "math.pi")
    return string
    
  def doRandom(self, string):
    while "rand(" in string:
      #Search for any time where there is rand(x,y)
      match = re.search("rand\((\d+),\s*(\d+)\)", string)
      #Index to locate position 
      start = string.find("rand(")
      end = string.find(")", start)
      #If rand(x,y) was found or not
      if match:
          #Assign min value and max value respectively
          min_value, max_value = match.groups()
          #Convert to integers
          min_value, max_value = int(min_value), int(max_value)
          result = str(random.randint(min_value, max_value))
          #Concatenate with the answer
          string = string[:start] + str(result) + string[end+1:]
    #Remove all appearances of rand(
    string = string.replace("rand(", "")
    return string

  def removeLeadingZero(self, string):
    #Pattern to remove leading zeros
    #leadingZerosPattern = r"0\d+"
    leadingZerosPattern = r"^0+(?=[1-9])"
    leadingZerosPatternTwo = r"(\d*\.\d+|\d+)"#r"(\d+)([+\-/*])(\d+)"
    #Pattern to allow for multiplication of adjacent brackets
    adjacentBracketsPattern = r"(\d+)(\([^)]+\))+"
    #string = re.sub(leadingZerosPattern, lambda x: x.group(0).lstrip("0"), string)
    string = re.sub(leadingZerosPatternTwo, lambda x: x.group(0).lstrip("0"), string)
    return string

  def replaceA(self, string):
    #Connect to the database
    self.conn = sqlite3.connect('variables.db')
    #Create a cursor to the database connection
    self.c = self.conn.cursor()
    #SQL command to fetch
    self.c.execute("SELECT value FROM variables WHERE name = ?", ("A"))
    #Get the first row from the query
    result = self.c.fetchone()
    #Get the first result of the above query
    value = result[0]
    #Replace all appearances of the character with the value
    while "A" in string:
      string = string.replace("A", str(value))
    return string

    conn.close()

  def replaceB(self, string):
    #Connect to the database
    self.conn = sqlite3.connect('variables.db')
    #Create a cursor to the database connection
    self.c = self.conn.cursor()
    #SQL command to fetch
    self.c.execute("SELECT value FROM variables WHERE name = ?", ("B"))
    #Get the first row from the query
    result = self.c.fetchone()
    #Get the first result of the above query
    value = result[0]
    #Replace all appearances of the character with the value
    while "B" in string:
      string = string.replace("B", str(value))
    return string

    conn.close()

  def replaceC(self, string):
    #Connect to the database
    self.conn = sqlite3.connect('variables.db')
    #Create a cursor to the database connection
    self.c = self.conn.cursor()
    #SQL command to fetch
    self.c.execute("SELECT value FROM variables WHERE name = ?", ("C"))
    #Get the first row from the query
    result = self.c.fetchone()
    #Get the first result of the above query
    value = result[0]
    #Replace all appearances of the character with the value
    while "C" in string:
      string = string.replace("C", str(value))
    return string

    conn.close()

  def replaceX(self, string):
    #Connect to the database
    self.conn = sqlite3.connect('variables.db')
    #Create a cursor to the database connection
    self.c = self.conn.cursor()
    #SQL command to fetch
    self.c.execute("SELECT value FROM variables WHERE name = ?", ("X"))
    #Get the first row from the query
    result = self.c.fetchone()
    #Get the first result of the above query
    value = result[0]
    #Replace all appearances of the character with the value
    while "X" in string:
      string = string.replace("X", str(value))
    return string

    conn.close()

  def replaceY(self, string):
    #Connect to the database
    self.conn = sqlite3.connect('variables.db')
    #Create a cursor to the database connection
    self.c = self.conn.cursor()
    #SQL command to fetch
    self.c.execute("SELECT value FROM variables WHERE name = ?", ("Y"))
    #Get the first row from the query
    result = self.c.fetchone()
    #Get the first result of the above query
    value = result[0]
    #Replace all appearances of the character with the value
    while "Y" in string:
      string = string.replace("Y", str(value))
    return string

    conn.close()
    

  def openSUVATWindow(self):
        class SUVAT(tk.Tk):
            def __init__(self):
                #Initialising the window
                tk.Tk.__init__(self)
                self.title("SUVAT Calculator")
                #400 width 150 depth
                self.geometry("400x150")
                self.create_widgets()

            def create_widgets(self):
                #Define all 3 displacement labels and boxes
                #Indicate the contents of the row
                self.labelS = tk.Label(self, text="S (Displacement)")
                self.labelS.grid(row=0, column=0)
                #Entry box for displacement
                self.entryS = tk.Entry(self)
                self.entryS.grid(row=0, column=1)
                #Ouput box if displacement is missing
                self.label2S = tk.Label(self, text="")
                self.label2S.grid(row=0, column=2)

                #Define all 3 initial velocity labels and boxes
                #Indicate the contents of the row
                self.labelU = tk.Label(self, text="U (Initial Velocity)")
                self.labelU.grid(row=1, column=0)
                #Entry box for initial velocity
                self.entryU = tk.Entry(self)
                self.entryU.grid(row=1, column=1)
                #Output box if initial velocity is missing
                self.label2U = tk.Label(self, text="")
                self.label2U.grid(row=1, column=2)

                #Define all 3 final velocity labels and boxes
                #Indicate the contents of the row
                self.labelV = tk.Label(self, text="V (Final Velocity)")
                self.labelV.grid(row=2, column=0)
                #Entry box for final velocity
                self.entryV = tk.Entry(self)
                self.entryV.grid(row=2, column=1)
                #Output box if final velocity is missing
                self.label2V = tk.Label(self, text="")
                self.label2V.grid(row=2, column=2)

                #Define all 3 acceleration labels and boxes
                #Indicate the contents of the row
                self.labelA = tk.Label(self, text="A (Acceleration)")
                self.labelA.grid(row=3, column=0)
                #Entry box for acceleration
                self.entryA = tk.Entry(self)
                self.entryA.grid(row=3, column=1)
                #Output box if acceleration is missing
                self.label2A = tk.Label(self, text="")
                self.label2A.grid(row=3, column=2)

                #Define all 3 time taken labels and boxes
                #Indicate the contents of the row
                self.labelT = tk.Label(self, text="T (Time Taken)")
                self.labelT.grid(row=4, column=0)
                #Entry box for time taken
                self.entryT = tk.Entry(self)
                self.entryT.grid(row=4, column=1)
                #Output box if time taken is missing
                self.label2T = tk.Label(self, text="")
                self.label2T.grid(row=4, column=2)

                #Define the calculate button and what command it runs when pressed
                self.calculateButton = tk.Button(self, text="Calculate", command=self.onCalculate)
                self.calculateButton.grid(row=5, column=1)
                
            def onCalculate(self):
                #Get all the values in the entry boxes
                s = self.entryS.get()
                u = self.entryU.get()
                v = self.entryV.get()
                a = self.entryA.get()
                t = self.entryT.get()

                if s == "":
                    if u == "":
                      try:
                        #If s and u are missing
                        v= float(v)
                        a= float(a)
                        t= float(t)
                        self.clearAll()
                        try:
                            #Calculating displacement
                            answer= str((v*t)-(0.5*a*t*t)) + "m"
                            self.label2S.config(text= answer)
                        except ZeroDivisionError:
                            self.label2S.config(text= "Zero Error")
                        except ValueError:
                            self.label2S.config(text= "Math Error")
                        try:
                            #Calculating initial velocity
                            answer2= str(v-(a*t)) + "m/s"
                            self.label2U.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2U.config(text= "Zero Error")
                        except ValueError:
                            self.label2U.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                            
                    if v == "":
                      try:
                        #If s and v are missing
                        u= float(u)
                        a= float(a)
                        t= float(t)
                        self.clearAll()
                        try:
                            #Calculating displacement
                            answer= str((u*t)+(0.5*a*t*t)) + "m"
                            self.label2S.config(text= answer)
                        except ZeroDivisionError:
                            self.label2S.config(text= "Zero Error")
                        except ValueError:
                            self.label2S.config(text= "Math Error")
                        try:
                            #Calculating final velocity
                            answer2= str(u+(a*t)) + "m/s"
                            self.label2V.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2V.config(text= "Zero Error")
                        except ValueError:
                            self.label2V.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                        
                    if a == "":
                      try:
                        #If s and a are missing
                        u= float(u)
                        v= float(v)
                        t= float(t)
                        self.clearAll()
                        try:
                            #Calculating displacement
                            answer= str((t/2)*(u+v)) + "m"
                            self.label2S.config(text= answer)
                        except ZeroDivisionError:
                            self.label2S.config(text= "Zero Error")
                        except ValueError:
                            self.label2S.config(text= "Math Error")
                        try:
                            #Calculating acceleration
                            answer2= str((v-u)/t) + "m/s^2"
                            self.label2A.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2A.config(text= "Zero Error")
                        except ValueError:
                            self.label2A.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                        
                    if t == "":
                      try:
                        #If s and t are missing
                        u= float(u)
                        v= float(v)
                        a= float(a)
                        self.clearAll()
                        try:
                            #calculating displacement
                            answer= str(((v*v)-(u*u))/(2*a)) + "m"
                            self.label2S.config(text= answer)
                        except ZeroDivisionError:
                            self.label2S.config(text= "Zero Error")
                        except ValueError:
                            self.label2S.config(text= "Math Error")
                        try:
                            #Calculating time taken
                            answer2= str((v-u)/a) + "s"
                            self.label2T.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2T.config(text= "Zero Error")
                        except ValueError:
                            self.label2T.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                            
                if u =="":
                    if a =="":
                      try:
                        #If u and a are missing
                        s= float(s)
                        v= float(v)
                        t= float(t)
                        self.clearAll()
                        try:
                            #Calculating initial velocity 
                            answer= str((2*s/t)-v) + "m/s"
                            self.label2U.config(text= answer)
                        except ZeroDivisionError:
                            self.label2U.config(text= "Zero Error")
                        except ValueError:
                            self.label2U.config(text= "Math Error")
                        try:
                            #Calculating acceleration
                            answer2= str((v*t-s)/(t*t*0.5)) + "m/s^2"
                            self.label2A.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2A.config(text= "Zero Error")
                        except ValueError:
                            self.label2A.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                        
                    if v =="":
                      try:
                        #if u and v are missing
                        s= float(s)
                        a= float(a)
                        t= float(t)
                        self.clearAll()
                        try:
                            #Calculating initial velocity
                            answer= str((s-0.5*a*t*t)/t) + "m/s"
                            self.label2U.config(text= answer)
                        except ZeroDivisionError:
                            self.label2U.config(text= "Zero Error")
                        except ValueError:
                            self.label2U.config(text= "Math Error")
                        try:
                            #Calculating final velocity
                            answer2= str((s+(0.5*a*t*t))/(t)) + "m/s"
                            self.label2V.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2V.config(text= "Zero Error")
                        except ValueError:
                            self.label2V.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                        
                    if t =="":
                      try:
                        #If u and t are missing
                        s= float(s)
                        v= float(v)
                        a= float(a)
                        self.clearAll()
                        try:
                            #Calculating initial velocity
                            answer= str(math.sqrt((v*v)-(2*a*s))) + "m/s"
                            self.label2U.config(text= answer)
                        except ZeroDivisionError:
                            self.label2U.config(text= "Zero Error")
                        except ValueError:
                            self.label2U.config(text= "Math Error")
                        try:
                            #Calculating time taken
                            answer2= str((-v-(math.sqrt((v*v)-(2*a*s))))/-a) + "s"
                            self.label2T.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2T.config(text= "Zero Error")
                        except ValueError:
                            self.label2T.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()

                if v =="":
                    if a== "":
                      try:
                        #If v and a are missing
                        s= float(s)
                        u= float(u)
                        t= float(t)
                        self.clearAll()
                        try:
                            #Calculating final velocity
                            answer= str((((2*s)/t)-u)) + "m/s"
                            self.label2V.config(text= answer)
                        except ZeroDivisionError:
                            self.label2V.config(text= "Zero Error")
                        except ValueError:
                            self.label2V.config(text= "Math Error")
                        try:
                            #Calculating acceleration
                            answer2= str((2*(s-(u*t)))/(t*t)) + "m/s^2"
                            self.label2A.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2A.config(text= "Zero Error")
                        except ValueError:
                            self.label2A.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                        
                    elif t =="":
                      try:
                        #If v and t are missing
                        s= float(s)
                        u= float(u)
                        a= float(a)
                        self.clearAll()
                        try:
                            #Calculating final velocity
                            answer= str(math.sqrt((u*u)+(2*a*s))) + "m/s"
                            self.label2V.config(text= answer)
                        except ZeroDivisionError:
                            self.label2V.config(text= "Zero Error")
                        except ValueError:
                            self.label2V.config(text= "Math Error")
                        try:
                            #Calculating time taken
                            answer2= str(((math.sqrt((2*a*s)+(u*u)))-u)/a) + "s"
                            self.label2T.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2T.config(text= "Zero Error")
                        except ValueError:
                            self.label2T.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()
                            
                if a =="":
                    if t== "":
                      try:
                        #If a and t are missing
                        s= float(s)
                        u= float(u)
                        v= float(v)
                        self.clearAll()
                        try:
                            #Calculating acceleration
                            answer= str(((v*v)-(u*u))/(2*s)) + "m/s^2"
                            self.label2A.config(text= answer)
                        except ZeroDivisionError:
                            self.label2A.config(text= "Zero Error")
                        except ValueError:
                            self.label2A.config(text= "Math Error")
                        try:  
                            #Calculating time taken
                            answer2= str((2*s)/(u+v)) + "s"
                            self.label2T.config(text= answer2)
                        except ZeroDivisionError:
                            self.label2T.config(text= "Zero Error")
                        except ValueError:
                            self.label2T.config(text= "Math Error")
                      except ValueError:
                        self.lessThanThree()

                count = 0
                for entry in (s, u, v, a, t):
                    if entry!= "":
                        count += 1
                #If there are not exactly 3 boxes filled
                if count != 3:
                    self.label2S.config(text= "Enter only 3 values")
                    self.label2U.config(text= "Enter only 3 values")
                    self.label2V.config(text= "Enter only 3 values")
                    self.label2A.config(text= "Enter only 3 values")
                    self.label2T.config(text= "Enter only 3 values")

            def lessThanThree(self):
                #If there are less than three boxes filled then tell the user
                self.label2S.config(text= "Enter only 3 values")
                self.label2U.config(text= "Enter only 3 values")
                self.label2V.config(text= "Enter only 3 values")
                self.label2A.config(text= "Enter only 3 values")
                self.label2T.config(text= "Enter only 3 values")

            def clearAll(self):
                #Clear the output labels
                self.label2S.config(text= "")
                self.label2U.config(text= "")
                self.label2V.config(text= "")
                self.label2A.config(text= "")
                self.label2T.config(text= "")
                

        if __name__ == "__main__":
                app = SUVAT()
                app.mainloop()


  def openQuadWindow(self):
    class EquationSolver(tk.Tk):
        def __init__(self):
            #Call the constructor of Tk class to initialise the window
            tk.Tk.__init__(self)
            #Set the title and size of the window
            self.title("Equation Solver")
            self.geometry("550x120")
            #Create widgets in the window
            self.createWidgets()
         
        def createWidgets(self):
            #Create labels and entry fields for a, b, and c of quadratic equation
            self.aLabel = tk.Label(self, text="a: (Coefficient of x^2)")
            self.aLabel.grid(row=0, column=0)
            self.aEntry = tk.Entry(self)
            self.aEntry.grid(row=0, column=1)

            self.bLabel = tk.Label(self, text="b: (Coefficient of x)")
            self.bLabel.grid(row=1, column=0)
            self.bEntry = tk.Entry(self)
            self.bEntry.grid(row=1, column=1)

            self.cLabel = tk.Label(self, text="c: (y intercept)")
            self.cLabel.grid(row=2, column=0)
            self.cEntry = tk.Entry(self)
            self.cEntry.grid(row=2, column=1)

            #Create a calculate button
            self.calculateButton = tk.Button(self, text="Calculate", command=self.calculateQuadratic)
            self.calculateButton.grid(row=3, column=1)

            #Create a label to display the roots of quadratic equation
            self.resultLabel = tk.Label(self, text="")
            self.resultLabel.grid(row=4, column=1)

        def calculateQuadratic(self):
          #Check if a is missing or equal to zero
          if self.aEntry.get() == "" or self.aEntry.get() == 0:
              self.resultLabel.config(text= "")
              self.resultLabel.config(text= "Error. 'a' cannot be 0 or missing")
          else:
              #Check if b and c are missing
              if self.bEntry.get() == "" and self.cEntry.get() =="":
                  a = float(self.aEntry.get())
                  b= 0
                  c= 0
              #Check if b is missing
              elif self.bEntry.get() == "":
                  a = float(self.aEntry.get())
                  b = 0
                  try:
                      c = float(self.cEntry.get())
                  except ValueError:
                      self.resultLabel.config(text= "")
                      self.resultLabel.config(text="Only float values are allowed")
                      return
              #Check if c is missing
              elif self.cEntry.get() =="":
                  a = float(self.aEntry.get())
                  try:
                      b = float(self.bEntry.get())
                  except ValueError:
                      self.resultLabel.config(text= "")
                      self.resultLabel.config(text="Only float values are allowed")
                      return
                  c= 0
              else:
                  try:
                      a = float(self.aEntry.get())
                      b = float(self.bEntry.get())
                      c = float(self.cEntry.get())
                  except ValueError:
                      self.resultLabel.config(text= "")
                      self.resultLabel.config(text="Only float values are allowed")
                      return

          #Calculate discriminant of quadratic equation
          discriminant = b**2 - 4*a*c

          #Calculate roots of quadratic equation based on discriminant
          if discriminant > 0:
              root1 = (-b + math.sqrt(discriminant)) / (2*a)
              root2 = (-b - math.sqrt(discriminant)) / (2*a)
              self.resultLabel.config(text= "")
              self.resultLabel.config(text=f"The roots are {root1} and {root2}")
          elif discriminant == 0:
              root1 = (-b) / (2*a)
              self.resultLabel.config(text= "")
              self.resultLabel.config(text=f"The root is {root1}")
          else:
              self.resultLabel.config(text= "")
              self.resultLabel.config(text="The equation has no real roots")

    if __name__ == "__main__":
        app = EquationSolver()
        app.mainloop()


  def store(self):
    class Storage:
      def __init__(self, master):
          self.master = master
          #Set the title of the window
          self.master.title("Store Variable")
          
          #Check if the database file already exists
          dbExists = os.path.exists('variables.db')
          #Connect to the database
          self.conn = sqlite3.connect('variables.db')
          self.c = self.conn.cursor()
          #Create a database if it doesnt exist
          if not dbExists:
              self.createTable()

          #Create a label and entry box for the variable name
          self.nameLabel = tk.Label(self.master, text="Variable name:")
          self.nameLabel.pack()
          self.nameEntry = tk.Entry(self.master)
          self.nameEntry.pack()

          #Create a label and entry box for the variable value
          self.valueLabel = tk.Label(self.master, text="Value:")
          self.valueLabel.pack()
          self.valueEntry = tk.Entry(self.master)
          self.valueEntry.pack()

          #Create a button to store the variable
          self.storeButton = tk.Button(self.master, text="Store", command=self.storeVariable)
          self.storeButton.pack()

          #Create a label to confirm the storage of the variable
          self.resultLabel = tk.Label(self.master, text="")
          self.resultLabel.pack()


      def createTable(self):
          #Create a table to store the variables and their values
          self.c.execute('''CREATE TABLE variables
                             (name TEXT PRIMARY KEY, value REAL)''')

          #Preset variables with the alphabet and value 0
          alphabet = 'ABCXY'
          for letter in alphabet:
              self.c.execute("INSERT INTO variables (name, value) VALUES (?, ?)", (letter, 0))


      def storeVariable(self):
          #Prompt the user for the name of the variable
          name = self.nameEntry.get()
          #Check if the entered name is valid
          if name not in ["A", "B", "C", "X", "Y"]:
              self.resultLabel.config(text="Error: Invalid variable name")
              return
          #Prompt the user for the value they want to store
          value = self.valueEntry.get()
          # Convert the value to a float to check if it is a valid number
          try:
              float(value)  
          except ValueError:
              self.resultLabel.config(text="Only numbers can be stored")
              return
          #Update the value of the variable in the database
          self.c.execute("UPDATE variables SET value = ? WHERE name = ?", (value, name))
          self.conn.commit()
          #Confirm that the value was stored successfully
          self.resultLabel.config(text=f"Successfully stored value {value} for variable {name}")

      def close(self):
          #Close the connection to the database
          self.conn.close()

    root = tk.Tk()
    app = Storage(root)
    root.mainloop()

    

  def graphing(self):
    #Define the functions using numpy
    global sin
    sin = np.sin
    global cos
    cos = np.cos
    global tan
    tan = np.tan
    global cot
    cot = lambda x: 1/np.tan(x)
    global sec
    sec = lambda x: 1/np.cos(x)
    global csc
    csc = lambda x: 1/np.sin(x)

    global ln
    ln = np.log
    global log10
    log10 = np.log10
    global log2
    log2 = np.log2
    global pi
    pi = math.pi
    global e
    e = math.e
    global mod
    mod = np.abs

    class Graph:
        def __init__(self, master):
            self.master = master
            master.title("Graph")
            
            #Create a Label widget asking for a function
            self.inputLabel = tk.Label(master, text="Input function in terms of x:")
            self.inputLabel.pack()
            #Create an entry widget for the function
            self.inputEntry = tk.Entry(master)
            self.inputEntry.pack()

            #Create an Entry widget
            self.boundsLabel = tk.Label(master, text="Enter domain:")
            self.boundsLabel.pack()
            self.boundsFrame = tk.Frame(master)
            self.boundsFrame.pack()

            #Create a Label widget asking for the lower bound
            self.lowerBoundLabel = tk.Label(self.boundsFrame, text="Lower Bound:")
            self.lowerBoundLabel.pack(side=tk.LEFT)
            #Create an entry widget for the lower bound
            self.lowerBoundEntry = tk.Entry(self.boundsFrame)
            self.lowerBoundEntry.pack(side=tk.LEFT)

            #Create a Label widget asking for the upper bound
            self.upperBoundLabel = tk.Label(self.boundsFrame, text="Upper Bound:")
            self.upperBoundLabel.pack(side=tk.LEFT)
            #Create an entry widget for the upper bound
            self.upperBoundEntry = tk.Entry(self.boundsFrame)
            self.upperBoundEntry.pack(side=tk.LEFT)

            #Create an error label
            self.errorLabel = tk.Label(master, text="")
            self.errorLabel.pack()

            #Create a button to plot on the same plot
            self.showOnSamePlotButton = tk.Button(master, text="Show on Same Plot", command=self.plotOnSamePlot)
            self.showOnSamePlotButton.pack(side=tk.LEFT)
            #Create an entry widget on a new window
            self.newPlotButton = tk.Button(master, text="New Plot", command=self.plotOnNewPlot)
            self.newPlotButton.pack(side=tk.LEFT)

        def plotOnSamePlot(self):
            equation = self.inputEntry.get()
            lb = int(self.lowerBoundEntry.get())
            ub = int(self.upperBoundEntry.get())

            #Set up the x-axis range
            x = np.linspace(lb, ub, 1000)
            #Evaluate the expression for each x value
            try:
              y = eval(equation)
            except NameError:
              self.errorLabel.config(text= "Error. Incorrect expression")

            # Create the plot
            if not hasattr(self, "fig"):
                self.fig, self.ax = plt.subplots()
            self.ax.plot(x, y, label = equation)
            
            # Find the turning points
            dydx = np.gradient(y, x)
            turning_points = x[np.where(np.diff(np.sign(dydx)))[0]]
            turning_points_y = eval(equation.replace('x', 'turning_points'))
            self.ax.plot(turning_points, turning_points_y, 'ro')
            # Find the x-intercepts
            x_intercepts = x[np.where(np.diff(np.sign(y)))[0]]
            x_intercepts_y = np.zeros_like(x_intercepts)
            self.ax.plot(x_intercepts, x_intercepts_y, 'go')
            # Find the y-intercept
            y_intercept = eval(equation.replace('x', '0'))
            self.ax.plot(0, y_intercept, 'bo')
            # Add the coordinates of x-intercepts to the plot
            for i, xi in enumerate(x_intercepts):
                self.ax.annotate(f"({xi:.2f}, {x_intercepts_y[i]:.2f})", (xi, x_intercepts_y[i]), 
                            textcoords="offset points", xytext=(0, 10), ha='center')
            # Add the coordinates of y-intercept to the plot
            self.ax.annotate(f"(0.00, {y_intercept:.2f})", (0, y_intercept), textcoords="offset points", 
                        xytext=(0, 10), ha='center')
            for i, tp in enumerate(turning_points):
                self.ax.annotate(f"({tp:.2f}, {turning_points_y[i]:.2f})", (tp, turning_points_y[i]), 
                            textcoords="offset points", xytext=(0, 10), ha='center')
            
            #Draw infinite x and y axes respectively
            self.ax.axhline(0, color='black', lw=0.5)
            self.ax.axvline(0, color='black', lw=0.5)
            # Add legend
            self.ax.legend(loc = "upper right")
            # Show the plot
            plt.draw()
            plt.show()  


        def plotOnNewPlot(self):
            equation = self.inputEntry.get()
            lb = int(self.lowerBoundEntry.get())
            ub = int(self.upperBoundEntry.get())
            # Set up the x-axis range
            x = np.linspace(lb, ub, 1000)
            # Evaluate the expression for each x value
            try:
              y = eval(equation)
            except NameError:
              self.errorLabel.config(text= "Error. Incorrect expression")
            
            # Create the plot
            fig, ax = plt.subplots()
            ax.plot(x, y)
            
            # Find the turning points
            dydx = np.gradient(y, x)
            turning_points = x[np.where(np.diff(np.sign(dydx)))[0]]
            turning_points_y = eval(equation.replace('x', 'turning_points'))
            ax.plot(turning_points, turning_points_y, 'ro')
            # Find the x-intercepts
            x_intercepts = x[np.where(np.diff(np.sign(y)))[0]]
            x_intercepts_y = np.zeros_like(x_intercepts)
            ax.plot(x_intercepts, x_intercepts_y, 'go')
            # Find the y-intercept
            y_intercept = eval(equation.replace('x', '0'))
            ax.plot(0, y_intercept, 'bo')
            # Add the coordinates of x-intercepts to the plot
            for i, xi in enumerate(x_intercepts):
                ax.annotate(f"({xi:.2f}, {x_intercepts_y[i]:.2f})", (xi, x_intercepts_y[i]), 
                            textcoords="offset points", xytext=(0, 10), ha='center')
            # Add the coordinates of y-intercept to the plot
            ax.annotate(f"(0.00, {y_intercept:.2f})", (0, y_intercept), textcoords="offset points", 
                        xytext=(0, 10), ha='center')
            for i, tp in enumerate(turning_points):
                ax.annotate(f"({tp:.2f}, {turning_points_y[i]:.2f})", (tp, turning_points_y[i]), 
                            textcoords="offset points", xytext=(0, 10), ha='center')
            
            #Draw infinite x and y axes respectively
            ax.axhline(0, color='black', lw=0.5)
            ax.axvline(0, color='black', lw=0.5)
            # Set the axis labels
            ax.set_xlabel('x')
            ax.set_ylabel('y')
            ax.set_title(f"y = {equation}")
            
            # Show the plot
            plt.show()


    if __name__ == "__main__":
        root = tk.Tk()
        gui = Graph(root)
        root.mainloop()


# Create the main window
root = tk.Tk()
root.title("Multi-Use Calculator")

# Create the calculator object and pack it into the main window
calc = Calculator(root)

# Run the Tkinter event loop
root.mainloop()
