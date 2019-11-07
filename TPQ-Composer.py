import os, sys
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidgetItem, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi
import matplotlib.pyplot as plt

#for pyinstaller to make standalone app with ui file
def resource_path(relative_path):
  if hasattr(sys, '_MEIPASS'):
      return os.path.join(sys._MEIPASS, relative_path)
  return os.path.join(os.path.abspath('.'), relative_path)

class Test(QDialog):
    def __init__(self):
       super(Test, self).__init__()
       loadUi(resource_path("./TPQ-Composer-GUI.ui"), self)
       
       self.setWindowTitle("TPQ Composer")
       #self.makeGraphButton.clicked.connect(self.on_makeGraphButton_clicked)
       self.removeRowButton.clicked.connect(self.removeRow)
       self.addRowButton.setEnabled(False)
       self.removeRowButton.setEnabled(False)
       self.makeGraphButton.setEnabled(False)
       self.makeCSVButton.setEnabled(False)
       self.strataSet=False
       self.kingsSet=False
       self.datesSet=False
       self.FIGURE_TITLE=""
       self.strata = []        
       self.kings  = [] 
       self.king_dates = []
       self.artifacts = {} 
       
       self.steps_x=[]
       self.steps_y=[]
       self.points_x=[]
       self.points_y=[]
       self.strata_numbers = []
       self.kings_numbers = []
#       
       self.POINTS_COLOR = ''          #color of the points
       self.STEP_FUNCTION_COLOR = ''   #color of the step function
       self.DPI = 300                     #DPI of the artifacts graph
       self.ARTIFACTS_GRAPH_FILENAME = 'artifacts-.png' #filename of the artifacts graph
       self.TPQS_FILENAME = ''                       #filename of the TPQ csv file
       self.X_AXIS_LABEL = ''         #label of the X axis
       self.Y_AXIS_LABEL = ''         #label of the Y axis
       
       header = self.artifactTable.horizontalHeader()       
       header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
       header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)
       header.setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)

    @pyqtSlot()
    def on_makeGraphButton_clicked(self):
        self.getAllValuesFromArtifactTable() 
        self.getValuesFromFields() 
        self.computeAllData()
        self.make_graph()
        QMessageBox.about(self, "Message", "The artifacts graph has been generated successfully.")
        
    @pyqtSlot()
    def on_makeCSVButton_clicked(self):
        self.getAllValuesFromArtifactTable() 
        self.getValuesFromFields()
        self.computeAllData()
        self.makeCSV()#self.steps_y)
        QMessageBox.about(self, "Message", "The CSV file has been generated successfully.")

       
    def createStrataComboBox(self):
        combo = QtWidgets.QComboBox()
        for stratum in self.strata:
            combo.addItem(stratum)       
        return combo
    
    def createKingsComboBox(self):
        combo = QtWidgets.QComboBox()
        for king in self.kings:
            combo.addItem(king)        
        return combo
    
    def getValuesFromFields(self):
        self.FIGURE_TITLE = self.graphTitleEdit.text()        
        self.POINTS_COLOR = self.pointsColorEdit.text()          #color of the points
        self.STEP_FUNCTION_COLOR = self.stepFctColorEdit.text()   #color of the step function
        self.DPI = int(self.dpiEdit.text())                    #DPI of the artifacts graph
        self.ARTIFACTS_GRAPH_FILENAME = self.graphFilenameEdit.text() #filename of the artifacts graph
        self.TPQS_FILENAME = self.tpqFilenameEdit.text()                     #filename of the TPQ csv file
        self.X_AXIS_LABEL = self.xLabelEdit.text()         #label of the X axis
        self.Y_AXIS_LABEL = self.yLabelEdit.text()          #label of the Y axis
    

        
    def enableButtons(self):
        if self.strataSet and self.kingsSet and self.datesSet:
            self.addRowButton.setEnabled(True)
            self.removeRowButton.setEnabled(True)
            self.makeGraphButton.setEnabled(True)
            self.makeCSVButton.setEnabled(True)
            
    @pyqtSlot()
    def on_setStrataButton_clicked(self):
        self.strata = [x.strip() for x in self.strataEdit.text().split(",")]
        self.artifactTable.setCellWidget(0, 0, self.createStrataComboBox())
        self.strataSet=True
        self.enableButtons()
        
    @pyqtSlot()
    def on_setKingsButton_clicked(self):
        self.kings = [x.strip() for x in self.kingsEdit.text().split(",")]
        self.artifactTable.setCellWidget(0, 1, self.createKingsComboBox())
        self.artifactTable.setItem(0, 2,QTableWidgetItem("1"))
        self.kingsSet=True
        self.enableButtons()
        
    @pyqtSlot()
    def on_setKingsDatesButton_clicked(self):
        self.king_dates = [int(x) for x in self.kingDatesEdit.text().split(",")]
        self.datesSet=True
        self.enableButtons()
            
    @pyqtSlot()
    def on_addRowButton_clicked(self):
        rowNumber = self.artifactTable.rowCount()
        self.artifactTable.insertRow(rowNumber)
        self.artifactTable.setCellWidget(rowNumber, 0, self.createStrataComboBox())
        self.artifactTable.setCellWidget(rowNumber, 1, self.createKingsComboBox())
        self.artifactTable.setItem(rowNumber, 2,QTableWidgetItem("1"))
                    
    def removeRow(self):        
        self.artifactTable.removeRow(self.artifactTable.currentRow())
        
    def getAllValuesFromArtifactTable(self):
        self.artifacts={}
        for i in range(self.artifactTable.rowCount()):
            stratum = self.artifactTable.cellWidget(i, 0).currentText()
            king = self.artifactTable.cellWidget(i, 1).currentText()
            occurences = int(self.artifactTable.item(i,2).text())
            if stratum not in self.artifacts.keys() :
                self.artifacts[stratum]=[(king, occurences)]
            else:
                self.artifacts[stratum].append((king, occurences))
        
    def has_point(self,x, y, ppoints_x, ppoints_y):
        for i in range(len(ppoints_x)):
            if(ppoints_x[i]==x and ppoints_y[i]==y):
                return True
        return False

    def get_robustness(self,x, y, ppoints_x, ppoints_y):
        for i in range(len(ppoints_x)):
            if(ppoints_x[i]==x and ppoints_y[i]==y):
                return self.points_nbr[i]
        return 0 
    
    def computeAllData(self):
        strata_d={} # dictionary assigning each stratum to a natural number, starting with 1
        i=1
        for stratum in self.strata:
            strata_d[stratum]=i
            i=i+1

        self.strata_numbers = list(strata_d.values())
        self.steps_x = self.strata_numbers[:]
        
        kings_d={} # dictionary assigning each stratum to a natural number, starting with 1
        i=1
        for king in self.kings:
            kings_d[king]=i
            i=i+1
        
        self.kings_numbers = list(kings_d.values()) 
        
        self.points_x = []
        self.points_y = []
        self.points_nbr = []
        for stratum in self.artifacts:
            for (king, nbr) in self.artifacts[stratum]:        
                self.points_x.append(strata_d[stratum])
                self.points_y.append(kings_d[king])
                self.points_nbr.append(nbr)
        
        self.steps_x = list((range(len(self.strata)+1)))
        del self.steps_x[0]
        self.steps_y=[]
        self.kings_numbers_2=[]
        for s in self.strata:
            if(s in self.artifacts):
                kings_vals = self.artifacts[s]
            else:
                kings_vals = []        
            self.kings_numbers_2.extend([kings_d[val[0]] for val in kings_vals])            
            max_king = max(self.kings_numbers_2)
            self.steps_y.append(max_king)          

            
    def make_graph(self) : 
        if len(self.kings) != len(self.king_dates):
            QMessageBox.about(self, "Error", "The number of kings and the number of earliest kings dates must match.")
            return
        
        fig, ax1 = plt.subplots(1,1)
        
        plt.title(self.FIGURE_TITLE)
        plt.xlabel(self.X_AXIS_LABEL)
        plt.ylabel(self.Y_AXIS_LABEL)
        
        plt.grid(True)
        ax1.set_xticks(self.strata_numbers)
        ax1.set_xticklabels(self.strata, minor=False, rotation=0)
        
        kings_labels = self.kings[:]
        for i in range(len(kings_labels)):
            kings_labels[i] +=  " (beg. " + str(self.king_dates[i]) + ")"
        ax1.set_yticks(self.kings_numbers)
        ax1.set_yticklabels(kings_labels, minor=False, rotation=0)   
        
        plt.plot(self.points_x, self.points_y, 'o', color=self.POINTS_COLOR)
        plt.plot(self.steps_x, self.steps_y, drawstyle='steps-post', color=self.STEP_FUNCTION_COLOR)
        
        y_offset=.2
        for i in range(len(self.points_x)):
            if(self.points_nbr[i] >1):
                plt.annotate('  ' + str(self.points_nbr[i]), xy=(self.points_x[i], self.points_y[i] + y_offset))            
        
        plt.savefig(self.ARTIFACTS_GRAPH_FILENAME, dpi=self.DPI, bbox_inches='tight')
        
    def makeCSV(self):
        
        output_file = open(self.TPQS_FILENAME,"w") 
        output_file.write("Stratum, TPQ, TPQ Date, Critical, Robustness\n")
        for i in range(len(self.strata)):
            output_file.write(self.strata[i]+", ")
            output_file.write("Stratum " + self.strata[i] + " ends after the start of " + self.kings[self.steps_y[i]-1] +", ")
            output_file.write(str(self.king_dates[self.steps_y[i]-1]) + ", ")
            robustness = 0
            
            if(i==0 or self.steps_y[i] > self.steps_y[i-1]):
                output_file.write("YES, ")
            else:
                output_file.write("NO, ")
            for x in range(1, i+2):
                for y in range(self.steps_y[i], len(self.kings)+1):
                    if(self.has_point(x, y, self.points_x, self.points_y)):
                        robustness = robustness + self.get_robustness(x, y, self.points_x, self.points_y)
            output_file.write(str(robustness))
            output_file.write("\n")

app=QApplication(sys.argv) 
widget=Test()
widget.show()
sys.exit(app.exec())      