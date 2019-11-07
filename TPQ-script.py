import matplotlib.pyplot as plt

###############################################################################
###  Script for producing an artifacts graph and a list of termini post     ###
###  quem on the basis of a list of strata, kings, kings' start dates       ###
###  and stratified artifacts bearing royal names (see: Levy, Piasetsky     ###
###  and Finkelstein,"Strata, Scarabs and Sycnhronisms: a Framework for     ###
###  Synchronizing Strata and Artifacts", in preparation).                  ###
###  The script produces the artifacts graph as file "artifacts-graph.png"  ###
###  and the list of TPQs as file "TPQs.csv".                               ###  
###  Author: Eythan Levy (eythan.levy@gmail.com), October 2019.             ###
###############################################################################

###############################################################################
############# HEADER: please encode your data here.               #############
############# Delete the values given below, meant as an example. #############
###############################################################################

#Type here the title of the figure
FIGURE_TITLE = 'Beth Shean scarabs'

### Encode the list of strata hereunder, from the earliest to the latest 
strata = ["XB","XA", "IXB", "IXA", "VIII", "VII", "VI", "Late VI"]

### Encode the list of kings hereunder, from the earliest to the latest 
kings  = ["Sesostris I", "Neferhotep I", "Hatshepsut", "Thutmosis III", 
         "Thutmosis IV", "Amenhophis III", "Ramesses I", "Ramesses II", 
         "Ramesses III", "Ramesses IV"]

### Encode the list of start of reign dates of all kings hereunder, from the earliest to the latest 
king_dates = [-1953, -1749, -1479, -1479, -1401, -1391, -1295, -1279, -1184, -1153]

### Encode hereunder, for each stratum, the list of kings whose artifacts were 
### found in this stratum (see also article mentionned above for 
### generalisations to this rule). Each king is to be supplied with the number
### of artifacts belonging to the stratum.
### Make sure to respect the given syntax: the python dictionary associates a 
### list of artifacts to each stratum. This list is a list of tuples, where 
### each tuple contains the name of the king and the number of corresponding 
### artifacts.

artifacts = { 
        "XB" : [("Neferhotep I", 1)],
        "IXA" : [("Sesostris I", 1), ("Thutmosis III", 3), ("Thutmosis IV", 1)], 
        "VIII" : [("Hatshepsut", 1), ("Thutmosis III", 1), ("Amenhophis III", 1), ("Ramesses I", 3)],
        "VII" : [("Thutmosis III", 1), ("Amenhophis III", 1), ("Ramesses I", 1), ("Ramesses II", 2)],
        "VI" : [("Thutmosis III", 1), ("Amenhophis III", 2), ("Ramesses II", 3), ("Ramesses III", 1), ("Ramesses IV", 1)],
        "Late VI" : [("Thutmosis III", 2), ("Thutmosis IV", 1)]         
        }

###############################################################################
############# Miscellaneous parameters: change below ONLY if you want #########
############# want to change the default behavior of the script.      #########
###############################################################################
POINTS_COLOR = 'red'          #color of the points
STEP_FUNCTION_COLOR = 'red'   #color of the step function
DPI = 300                     #DPI of the artifacts graph
ARTIFACTS_GRAPH_FILENAME = 'artifacts-graph.png' #filename of the artifacts graph
TPQS_FILENAME = 'TPQs.csv'                       #filename of the TPQ csv file
X_AXIS_LABEL = 'Latest possible stratum'         #label of the X axis
Y_AXIS_LABEL = 'Earliest possible reign'         #label of the Y axis

###############################################################################
############# DO NOT EDIT BELOW THIS POINT ####################################
###############################################################################

def has_point(x, y, points_x, points_y):
    for i in range(len(points_x)):
        if(points_x[i]==x and points_y[i]==y):
            return True
    return False

def get_robustness(x, y, points_x, points_y):
    for i in range(len(points_x)):
        if(points_x[i]==x and points_y[i]==y):
            return points_nbr[i]
    return 0 

strata_d={} # dictionary assigning each stratum to a natural number, starting with 1
i=1
for stratum in strata:
    strata_d[stratum]=i
    i=i+1

#strata_numbers = list((range(len(strata)+1))) #list of stratum numbers (starting at 1)
#del strata_numbers[0] #removing 0 to make the list statr at 1

strata_numbers = list(strata_d.values())

#steps_x = list((range(len(strata)+1))) # steps (x coordinates) of the step function
#del steps_x[0]
steps_x = strata_numbers[:]

kings_d={} # dictionary assigning each stratum to a natural number, starting with 1
i=1
for king in kings:
    kings_d[king]=i
    i=i+1

kings_numbers = list(kings_d.values()) 

points_x = []
points_y = []
points_nbr = []
for stratum in artifacts:
    for (king, nbr) in artifacts[stratum]:        
        points_x.append(strata_d[stratum])
        points_y.append(kings_d[king])
        points_nbr.append(nbr)
        
    
fig, ax1 = plt.subplots(1,1)

plt.title(FIGURE_TITLE)
plt.xlabel(X_AXIS_LABEL)
plt.ylabel(Y_AXIS_LABEL)

plt.grid(True)
ax1.set_xticks(strata_numbers)
ax1.set_xticklabels(strata, minor=False, rotation=0)

kings_labels = kings[:]
for i in range(len(kings_labels)):
    kings_labels[i] +=  " (beg. " + str(king_dates[i]) + ")"
ax1.set_yticks(kings_numbers)
ax1.set_yticklabels(kings_labels, minor=False, rotation=0)

plt.plot(points_x, points_y, 'o', color=POINTS_COLOR)

steps_x = list((range(len(strata)+1)))
del steps_x[0]
steps_y=[]
kings_numbers=[]
for s in strata:
    if(s in artifacts):
        kings_vals = artifacts[s]
    else:
        kings_vals = []        
    kings_numbers.extend([kings_d[val[0]] for val in kings_vals])

    steps_y.append(max(kings_numbers))
plt.plot(steps_x, steps_y, drawstyle='steps-post', color=STEP_FUNCTION_COLOR)

y_offset=.2
for i in range(len(points_x)):
    if(points_nbr[i] >1):
        plt.annotate('  ' + str(points_nbr[i]), xy=(points_x[i], points_y[i] + y_offset))    


plt.savefig(ARTIFACTS_GRAPH_FILENAME, dpi=DPI, bbox_inches='tight')

# MAKE CSV file
output_file = open(TPQS_FILENAME,"w") 
output_file.write("Stratum, TPQ, TPQ Date, Critical, Robustness\n")
for i in range(len(strata)):
    output_file.write(strata[i]+", ")
    output_file.write("Stratum " + strata[i] + " ends after the start of " + kings[steps_y[i]-1] +", ")
    output_file.write(str(king_dates[steps_y[i]-1]) + ", ")
    robustness = 0
    if(i==0 or steps_y[i] > steps_y[i-1]):
        output_file.write("YES, ")
    else:
        output_file.write("NO, ")
    for x in range(1, i+2):
        for y in range(steps_y[i], len(kings)+1):
            if(has_point(x, y, points_x, points_y)):
                robustness = robustness + get_robustness(x, y, points_x, points_y)
    output_file.write(str(robustness))
    output_file.write("\n")
