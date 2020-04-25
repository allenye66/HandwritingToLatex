
# %% [code]
a = ['beta','neq','x','6','div','4','+','(','9','-','infinity', 'theta', 'int', '2', 'e', 'a', '8', '1', '7', 'y', '!', 'times', '5','pm', 'pi', '0', 'z', '3', 'alpha', 'j', ')','=']

# %% [code]
myDict = { "beta": "\beta",
            "neq": "\neq",
            "x": "x",
            "6": "6",
            "div": "\div",
            "4": "4",
            "+": "+",   
            "(": "( \,",
            "9": "9",
            "-": "-",
            "infinity": "\infty",
            "theta":"\theta ",
          "int": "\int",
          "2": "2",
          "e": "e",
          "a": "a",
          "8": "8",
          "1": "1",
          "7": "7",
          "y": "y",
          "!": "!",
          "times": "\times",
            "5": "5",
          "pm": "\pm",
          "pi": "\pi",
          "0": "\theta",
          "z": "z",
          "3": "3",
        "alpha": "\alpha",
          "j": "j",
          ")": ") \,",
          "=":"="
}


# %% [code]
str = "5 1 ( 6 8 x + 8 8 ) = y div 6"
result = "$"
spaces = [0]
for i in range(len(str)):
    if str[i] == " ":
        spaces.append(i)
spaces.append(len(str))
spaces

# %% [code]
result = "$"
for i in range(len(spaces)-1):
     result = result + myDict[(str[spaces[i]: spaces[i+1]]).replace(" ", "")]
result = result.replace(" ", "")
print(result)