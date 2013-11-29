from constraint import * #imports
problem = Problem()  #Create a blank problem where we can add solutions.
problem.addVariable('a', range(5+1)) #Add a variable named a, and specify its domain. Since a+b=5, a is a positive integer less than 5
problem.addVariable('b', range(5+1)) #Same thing with b
problem.addConstraint(lambda a, b: a + b == 5) # Tell the computer that a+b=5
problem.addConstraint(lambda a, b: a * b == 6) #tell the computer that a*b=6
problem.addConstraint(lambda a, b: a > b) #tell the computer that a*b=6
print problem.getSolutions() #We are done, get the solutions.
