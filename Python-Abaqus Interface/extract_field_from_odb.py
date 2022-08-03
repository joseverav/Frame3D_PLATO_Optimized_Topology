"""
Template script to extract field output from an odb.

Usage: abaqus python extract.py 
      -od odbName
      -st stepName
      -pr partInstanceName
      -no nodeNumber
      -ns NodeSetName
      -fo FieldoutputVariableIdentifier
      -ou outputFileName

The script prompts user to enter a different file name if the output file already exists.

An example usage is given below:
abaqus python extract_field_from_odb.py -od Job-1 -st Step-1 -pr PART-1-1 -no 5 -fo RF3 -ou output.txt      
"""

import os
from sys import argv, exit
import odbAccess
from abaqusConstants import TRUE

#=================================================================
def rightTrim(input,suffix):
    if (input.find(suffix) == -1):
        input = input + suffix
    return input

#=================================================================
def outputToText(paramList):

    odbName = paramList[0]
    stepname = paramList[1]
    partInstance = paramList[2]
    nId = paramList[3]
    fieldOutputRequest = paramList[4]
    outputFile = paramList[5]
    nodeSet = paramList[6]
    
    if stepName not in odb.steps.keys():
        print 'Error: The step %s does not exist in odb %s\n'\
              '\tCheck for the case in the step name.' %(stepName, odbName)
        odb.close()
        return

    if partInstance not in odb.rootAssembly.instances.keys():
        print 'Error: The part instance "%s" does not exist in the odb.\n'\
              '\tCheck for the case of the part instance name.\n' %(partInstance)
        return
    
    odbStep = odb.steps[stepName]
    
    file1=open(outputFile,'w')
    file1.write("#Step %s\n" % stepname)
    data = []
    frame_ids = []
    
    if nId > 0:
        for odbFrame in odbStep.frames:
            n_obj = odb.rootAssembly.instances[partInstance].getNodeFromLabel(nId)
	    #e_obj = odb.rootAssembly.instances['PART-1-1'].getElementFromLabel(eId)

            subset = odbFrame.fieldOutputs[fieldOutputRequest].getSubset(region=n_obj)
	    #subset = odbFrame.fieldOutputs[fieldOutputRequest].getSubset(region=e_obj)
	    
            data.append(subset.values) 
	    
	    # for storing all gp values in the element
	    #for gp_results in subset.values:
	    #    data.append(gp_results.data)
	    
	    # or for doing only the centroid
	    #odbAccess.xyDataListFromField(odb=odb, outputPosition=ELEMENT_CENTROID,
            #        variable=((fieldOutputRequest, INTEGRATION_POINT), ), elementLabels=((partInstance, (
            #        eId, )), ))
	       
            frame_ids.append(odbFrame.frameId)        
        
    if nodeSet != None:
        for odbFrame in odbStep.frames:
            ns_obj = odb.rootAssembly.instances[partInstance].nodeSets[nodeSet]
            
            subset = odbFrame.fieldOutputs[fieldOutputRequest].getSubset(region=ns_obj)
            data.append(subset.values)
            frame_ids.append(odbFrame.frameId)
    
    for fidx,fid in enumerate(frame_ids):
        file1.write("#frame %s\n" % fid)
        for j in data[fidx]:
            line = ""
            for k in j.data:
                line += " %g" % k
            line += "\n"
            file1.write(line)
        

    file1.close()
    print 'Output successfully written to the file %s.\n' %(outputFile)
    odb.close()

#==================================================================
# S T A R T
#    
if __name__ == '__main__':    

    odbName = None
    stepName = None
    partInstance =None
    nodeList = None
    nodeSet = None
    historyOutputRequest = None
    fieldOutputRequest = None
    outputFile = None
    paramList = []
    i = 0
    argList = argv
    argCount = len(argList)
    nid = 0
    frameIdx = -1
    
    try:
        while (i < argCount):
            flag = argList[i][:3]
            if (flag == "-od"):
                i+=1
                name = argList[i]
                odbName = rightTrim(name, '.odb')
            elif (flag == "-st"):
                i+=1
                stepName = argList[i]
            elif (flag == "-pr"):
                i+=1
                partInstance = argList[i]
            elif (flag == "-no"):
                i+=1
                nid = int(argList[i])
            elif (flag == "-ns"):
                i+=1
                nodeSet = argList[i]
            elif (flag == "-fo"):
                i+=1
                fieldOutputRequest = argList[i]
            elif (flag == "-ou"):
                i+=1
                outputFile = argList[i]
            elif (flag == "-he"):
                print __doc__
                exit(0)
            i+=1   

        if None in (odbName, stepName, partInstance, fieldOutputRequest, outputFile):
            print "***ERROR: All required arguments are not provided"
            print __doc__
            exit(0)
                
    except IndexError:
        print "***ERROR: All required arguments are not provided"
        print __doc__
        exit(0)

    msg = 'The output file %s already exists. Do you want to overwrite\n'\
          'the existing file? (Y/N)\n' %(outputFile)
    msg1 = 'Please enter the file name to write the output.\n'
    positive = ['Y', 'YES']
    negative = ['N', 'NO']

    #Prompt user to enter a different output file name if the specified file already exists.
    if os.path.isfile(outputFile):
        response = raw_input(msg).strip()
        if response.upper() in negative:
            outputFile = raw_input(msg1).strip()
        elif response.upper() in positive:
            print 'The file %s will be overwritten.\n' % (outputFile)
        else:
            print 'Not a valid response.\n'
            exit(0)
    
    try: 
        odb=odbAccess.openOdb(path=odbName,readOnly=TRUE)
    except:
        print 'Error: Unable to open the specified odb %s' %(odbName)
            
    paramList = [odbName, stepName, partInstance, nid, 
                 fieldOutputRequest,outputFile,nodeSet]
    
    outputToText(paramList)
