import sys
import pandas as pd
import time, numpy as np
import pyomo.environ as pyo
from pyomo.environ import *
from pyomo.opt import SolverFactory

#Parameters

c = np.array([
    [90, 80, 75, 70],
    [35, 85, 55, 65],
    [125, 95, 90, 95],
    [45, 110, 95, 115],
    [50, 100, 90, 100]]) # assignment cost

n = len(c)    #number of workers
m = len(c[0]) #number of tasks 

range_i = range(0,n)
range_j = range(0,m)

#Create Model
model = pyo.ConcreteModel()

#Define variables
model.x = pyo.Var(range(n), # index i
                  range(m), # index j
                  within=Binary)
x = model.x

#Define Constraints

model.C1 = pyo.ConstraintList() # Each task is assigned to exactly one worker.
for j in range_j:
    model.C1.add(expr = sum([x[i,j] for i in range_i]) == 1)
    
model.C2 = pyo.ConstraintList() # Each worker is assigned to at most one task.
for i in range_i:
    model.C2.add(expr = sum([x[i,j] for j in range_j]) <= 1 )
    
# Define Objective Function
Total_Cost = sum(c[i][j]*x[i,j] for i in range_i for j in range_j)
model.obj = pyo.Objective(expr = Total_Cost, sense = minimize)

begin = time.time()
opt = SolverFactory('cplex')
results = opt.solve(model)

deltaT = time.time() - begin

model.pprint()

sys.stdout = open("Assignment_Problem_Results.txt", "w")
print('Time =', np.round(deltaT,2))


if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
    for i in range_i:
        for j in range_j:
            if pyo.value(x[i,j]) == 1.00:
              #print('x[',i,'][',j,'] ',pyo.value(x[i,j]))
               print('Assign worker ', i , 'to task ', j, ' with cost ', c[i][j])
    print('Objective Function value =', pyo.value(model.obj))
    print('Solver Status is =', results.solver.status)
    print('Termination Condition is =', results.solver.termination_condition)
elif (results.solver.termination_condition == TerminationCondition.infeasible):
   print('Model is unfeasible')
  #print('Solver Status is =', results.solver.status)
   print('Termination Condition is =', results.solver.termination_condition)
else:
    # Something else is wrong
    print ('Solver Status: ',  result.solver.status)
    print('Termination Condition is =', results.solver.termination_condition)
    
sys.stdout.close()