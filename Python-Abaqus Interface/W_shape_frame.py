# -*- coding: mbcs -*-
# Do not delete the following import lines
from abaqus import *
from abaqusConstants import *
import __main__
import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import os
import shutil

'''
PROGRAM TO CREATE, MESH, AND RUN JOB FOR W-SHAPE PORTAL FRAME
SUPPORT CONDITIONS: FIXED
LOAD TYPE = GRAVITY AND EARTHQUAKE
'''

# For W16x31 - Shape Properties - Units: Inches
# Beam
b_length = 180  # Beam length
b_depth = 15.9  # Beam depth, d
b_fwidth = 5.53  # Beam flange width, bf
b_fthick = 0.440  # Beam flange thickness, tf
b_wthick = 0.275  # Beam web thickness, tw
# Column
c_length = 120  # Column length
c_depth = 15.9  # Column depth, d
c_fwidth = 5.53  # Column flange width, bf
c_fthick = 0.440  # Column flange thickness, tf
c_wthick = 0.275  # Column web thickness, tw

# Loads - Pressures - Units: PSI
grav_load = 303.  # Gravity load on beam top flange
eq_load = 2287.  # Earthquake load on side of beam web

# Job Run Parameters
seed_no = [48, 24, 12, 6, 3, 1.5, 0.75]  # Number of global seeds
analysis_enviro = 1  # Use 1 for local machine, 2 for remote machine
job_name = 'trial_run'  # Folder must already be created with this name

# Environment Selection
if analysis_enviro == 1:  # Corresponds to local machine
    results_dir = 'C:/Users/Jose Vera/Documents/College/Fall 2020/Finite Elements' \
                  '/PROJECT/Python-Abaqus Interface/'
    home_dir = 'C:/Users/Jose Vera/Documents/College/ABAQUS/'
elif analysis_enviro == 2:  # Corresponds to remote UofU Finite Elements Pool 0
    results_dir = 'X:/Documents/'
    home_dir = 'C:/temp/'



'''W-SHAPE PART CREATION'''

'''SECTIONING'''
# Beam
s1 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                             sheetSize=200.0)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
# Set construction lines for mirror
s1.setPrimaryObject(option=STANDALONE)
s1.ConstructionLine(point1=(0.0, 0.0), angle=90.0)
s1.VerticalConstraint(entity=g[2], addUndoState=False)
s1.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
s1.HorizontalConstraint(entity=g[3], addUndoState=False)
# Draw first quadrant of section
s1.setPrimaryObject(option=STANDALONE)
s1.Line(point1=(b_wthick / 2, b_depth / 2), point2=(b_fwidth / 2, b_depth / 2))
s1.HorizontalConstraint(entity=g[4], addUndoState=False)
s1.Line(point1=(b_fwidth / 2, b_depth / 2), point2=(b_fwidth / 2, b_depth / 2 - b_fthick))
s1.VerticalConstraint(entity=g[5], addUndoState=False)
s1.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
s1.Line(point1=(b_fwidth / 2, b_depth / 2 - b_fthick), point2=(b_wthick / 2, b_depth / 2 - b_fthick))
s1.HorizontalConstraint(entity=g[6], addUndoState=False)
s1.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
s1.Line(point1=(b_wthick / 2, b_depth / 2 - b_fthick), point2=(b_wthick / 2, 0.0))
s1.VerticalConstraint(entity=g[7], addUndoState=False)
s1.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
# Mirror operations
s1.copyMirror(mirrorLine=g[2], objectList=(g[4], g[5], g[6], g[7]))
s1.Line(point1=(-b_wthick / 2, b_depth / 2), point2=(b_wthick / 2, b_depth / 2))
s1.HorizontalConstraint(entity=g[12], addUndoState=False)
s1.copyMirror(mirrorLine=g[3], objectList=(g[4], g[5], g[6], g[7],
                                           g[8], g[9], g[10], g[11], g[12]))
# Part parameter assignments
p = mdb.models['Model-1'].Part(name='BEAM', dimensionality=THREE_D,
                               type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['BEAM']
p.BaseSolidExtrude(sketch=s1, depth=b_length)

# Column
s2 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                             sheetSize=200.0)
g, v, d, c = s2.geometry, s2.vertices, s2.dimensions, s2.constraints
# Set construction lines for mirror
s2.setPrimaryObject(option=STANDALONE)
s2.ConstructionLine(point1=(0.0, 0.0), angle=90.0)
s2.VerticalConstraint(entity=g[2], addUndoState=False)
s2.ConstructionLine(point1=(0.0, 0.0), angle=0.0)
s2.HorizontalConstraint(entity=g[3], addUndoState=False)
# Draw first quadrant of section
s2.setPrimaryObject(option=STANDALONE)
s2.Line(point1=(b_wthick / 2, b_depth / 2), point2=(b_fwidth / 2, b_depth / 2))
s2.HorizontalConstraint(entity=g[4], addUndoState=False)
s2.Line(point1=(b_fwidth / 2, b_depth / 2), point2=(b_fwidth / 2, b_depth / 2 - b_fthick))
s2.VerticalConstraint(entity=g[5], addUndoState=False)
s2.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
s2.Line(point1=(b_fwidth / 2, b_depth / 2 - b_fthick), point2=(b_wthick / 2, b_depth / 2 - b_fthick))
s2.HorizontalConstraint(entity=g[6], addUndoState=False)
s2.PerpendicularConstraint(entity1=g[5], entity2=g[6], addUndoState=False)
s2.Line(point1=(b_wthick / 2, b_depth / 2 - b_fthick), point2=(b_wthick / 2, 0.0))
s2.VerticalConstraint(entity=g[7], addUndoState=False)
s2.PerpendicularConstraint(entity1=g[6], entity2=g[7], addUndoState=False)
# Mirror operations
s2.copyMirror(mirrorLine=g[2], objectList=(g[4], g[5], g[6], g[7]))
s2.Line(point1=(-b_wthick / 2, b_depth / 2), point2=(b_wthick / 2, b_depth / 2))
s2.HorizontalConstraint(entity=g[12], addUndoState=False)
s2.copyMirror(mirrorLine=g[3], objectList=(g[4], g[5], g[6], g[7],
                                           g[8], g[9], g[10], g[11], g[12]))
# Part parameter assignments
p = mdb.models['Model-1'].Part(name='COLUMN', dimensionality=THREE_D,
                               type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s2, depth=c_length)

# Base Plate
s3 = mdb.models['Model-1'].ConstrainedSketch(name='__profile__',
                                             sheetSize=200.0)
g, v, d, c = s3.geometry, s3.vertices, s3.dimensions, s3.constraints
s3.setPrimaryObject(option=STANDALONE)
s3.Line(point1=(-c_fwidth / 2, -c_depth / 2), point2=(c_fwidth / 2, -c_depth / 2))
s3.HorizontalConstraint(entity=g[2], addUndoState=False)
s3.Line(point1=(c_fwidth / 2, -c_depth / 2), point2=(c_fwidth / 2, c_depth / 2))
s3.VerticalConstraint(entity=g[3], addUndoState=False)
s3.PerpendicularConstraint(entity1=g[2], entity2=g[3], addUndoState=False)
s3.Line(point1=(c_fwidth / 2, c_depth / 2), point2=(-c_fwidth / 2, c_depth / 2))
s3.HorizontalConstraint(entity=g[4], addUndoState=False)
s3.PerpendicularConstraint(entity1=g[3], entity2=g[4], addUndoState=False)
s3.Line(point1=(-c_fwidth / 2, c_depth / 2), point2=(-c_fwidth / 2, -c_depth / 2))
s3.VerticalConstraint(entity=g[5], addUndoState=False)
s3.PerpendicularConstraint(entity1=g[4], entity2=g[5], addUndoState=False)
s3.PerpendicularConstraint(entity1=g[2], entity2=g[5], addUndoState=False)
# Part parameter assignments
p = mdb.models['Model-1'].Part(name='BASE-PLATE', dimensionality=THREE_D,
                               type=DEFORMABLE_BODY)
p.BaseSolidExtrude(sketch=s3, depth=1.0)

'''MATERIAL CREATION'''
# STEEL
mdb.models['Model-1'].Material(name='Steel')
mdb.models['Model-1'].materials['Steel'].Elastic(table=((29000000.0, 0.303),))

'''SECTION ASSIGNMENT'''
# Beam
mdb.models['Model-1'].HomogeneousSolidSection(name='Beam-Section',
                                              material='Steel', thickness=None)
p = mdb.models['Model-1'].parts['BEAM']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1f ]',), )
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='Beam-Section', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
# Column
mdb.models['Model-1'].HomogeneousSolidSection(name='Column-Section',
                                              material='Steel', thickness=None)
p = mdb.models['Model-1'].parts['COLUMN']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1f ]',), )
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='Column-Section', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)
# Base Plate
mdb.models['Model-1'].HomogeneousSolidSection(name='BP-Section',
                                              material='Steel', thickness=None)
p = mdb.models['Model-1'].parts['BASE-PLATE']
c = p.cells
cells = c.getSequenceFromMask(mask=('[#1f ]',), )
region = regionToolset.Region(cells=cells)
p.SectionAssignment(region=region, sectionName='BP-Section', offset=0.0,
                    offsetType=MIDDLE_SURFACE, offsetField='',
                    thicknessAssignment=FROM_SECTION)

'''PARTITIONING'''
p = mdb.models['Model-1'].parts['BEAM']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
f = p.faces
p.PartitionCellByExtendFace(extendFace=f[3], cells=pickedCells)
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#7 ]',), )
f1 = p.faces
p.PartitionCellByExtendFace(extendFace=f1[17], cells=pickedCells)

p = mdb.models['Model-1'].parts['COLUMN']
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#1 ]',), )
f = p.faces
p.PartitionCellByExtendFace(extendFace=f[3], cells=pickedCells)
c = p.cells
pickedCells = c.getSequenceFromMask(mask=('[#7 ]',), )
f1 = p.faces
p.PartitionCellByExtendFace(extendFace=f1[17], cells=pickedCells)

'''INSTANCES'''
# Create Instances
a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['BEAM']
a1.Instance(name='BEAM-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['COLUMN']
a1.Instance(name='COLUMN-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['COLUMN']
a1.Instance(name='COLUMN-2', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['BASE-PLATE']
a1.Instance(name='BASE-PLATE-1', part=p, dependent=ON)
p = mdb.models['Model-1'].parts['BASE-PLATE']
a1.Instance(name='BASE-PLATE-2', part=p, dependent=ON)
# Assemble Frame Geometry
a1.rotate(instanceList=('COLUMN-1', 'COLUMN-2',), axisPoint=(1.0, 0.0, 0.0),
          axisDirection=(-1.0, 0.0, 0.0), angle=-90.0)
a1.translate(instanceList=('COLUMN-1',), vector=(0.0, -(b_depth / 2), (c_depth / 2)))
a1.translate(instanceList=('COLUMN-2',), vector=(0.0, -(b_depth / 2), b_length - (c_depth / 2)))
a1.rotate(instanceList=('BASE-PLATE-1', 'BASE-PLATE-2',), axisPoint=(1.0, -(b_depth / 2), 0.0),
          axisDirection=(-1.0, 0.0, 0.0), angle=-90.0)
a1.translate(instanceList=('BASE-PLATE-1',), vector=(0.0, -c_length, 0.0))
a1.translate(instanceList=('BASE-PLATE-2',), vector=(0.0, -c_length, b_length - (c_depth)))
# Merge geometries to create new part FRAME
a1.InstanceFromBooleanMerge(name='FRAME', instances=(a1.instances['BEAM-1'],
                                                     a1.instances['COLUMN-1'], a1.instances['COLUMN-2'],
                                                     a1.instances['BASE-PLATE-1'], a1.instances['BASE-PLATE-2'],),
                            keepIntersections=ON, originalInstances=SUPPRESS, domain=GEOMETRY)

'''BOUNDARY CONDITIONS'''
# Fixed Supports
a = mdb.models['Model-1'].rootAssembly
f1 = a.instances['FRAME-1'].faces
faces1 = f1.getSequenceFromMask(mask=('[#1020 ]',), )
region = regionToolset.Region(faces=faces1)
mdb.models['Model-1'].DisplacementBC(name='FIXED', createStepName='Initial',
                                     region=region, u1=SET, u2=SET, u3=SET, ur1=SET, ur2=SET, ur3=SET,
                                     amplitude=UNSET, distributionType=UNIFORM, fieldName='',
                                     localCsys=None)
# Loads on Frame
# Gravity load on beam
mdb.models['Model-1'].StaticStep(name='Loads', previous='Initial',
                                 description='Applied Loads on Frame')
s1 = a.instances['FRAME-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#0:2 #20000000 ]',), )
region = regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].Pressure(name='Applied Pressure', createStepName='Loads',
                               region=region, distributionType=UNIFORM, field='', magnitude=grav_load,
                               amplitude=UNSET)
# Earthquake load on side of beam
s1 = a.instances['FRAME-1'].faces
side1Faces1 = s1.getSequenceFromMask(mask=('[#0:2 #4000000 ]',), )
region = regionToolset.Region(side1Faces=side1Faces1)
mdb.models['Model-1'].Pressure(name='EQ', createStepName='Loads',
                               region=region, distributionType=UNIFORM, field='', magnitude=eq_load,
                               amplitude=UNSET)

'''FOR LOOP FOR MULTIPLE JOB CREATION WITH DIFFERENT CONDITIONS'''
# Condition to change: Global seeds

for i in range(len(seed_no)):

    '''SEEDING'''
    p = mdb.models['Model-1'].parts['FRAME']
    e = p.edges
    pickedEdges = e.getSequenceFromMask(mask=('[#ffffffff:6 #3f ]',), )
    p.seedEdgeBySize(edges=pickedEdges, size=seed_no[i], deviationFactor=0.1)
    elemType1 = mesh.ElemType(elemCode=C3D20R, elemLibrary=STANDARD)
    elemType2 = mesh.ElemType(elemCode=C3D15, elemLibrary=STANDARD)
    elemType3 = mesh.ElemType(elemCode=C3D10, elemLibrary=STANDARD,
                              secondOrderAccuracy=OFF, distortionControl=DEFAULT)
    c = p.cells
    cells = c.getSequenceFromMask(mask=('[#1ffff ]',), )
    pickedRegions = (cells,)
    # Set element type to quadratic tetrahedron
    if i == 0:
        p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2,
                                                           elemType3))
    p.generateMesh()
    # Replace period in decimal with "_"
    if seed_no[i] < 2:
        seed_str = str(seed_no[i]).replace(".", "_")
    else:
        seed_str = str(seed_no[i])

    '''JOB CREATION'''
    mdb.Job(name=job_name + seed_str, model='Model-1', description='', type=ANALYSIS,
            atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90,
            memoryUnits=PERCENTAGE, getMemoryFromAnalysis=True,
            explicitPrecision=SINGLE, nodalOutputPrecision=SINGLE, echoPrint=OFF,
            modelPrint=OFF, contactPrint=OFF, historyPrint=OFF, userSubroutine='',
            scratch='', resultsFormat=ODB)
    mdb.jobs[job_name + seed_str].submit(consistencyChecking=OFF)
    mdb.jobs[job_name + seed_str].waitForCompletion()

    '''POST-PROCESSING'''
    # Set viewport zoom and perspective
    jobPath = job_name + seed_str + '.odb'
    odb_object = session.openOdb(name=jobPath)
    session.viewports['Viewport: 1'].setValues(displayedObject=odb_object)
    session.viewports['Viewport: 1'].view.setViewpoint(viewVector=(1, 0, 0),
                                                       cameraUpVector=(0, 1, 0))
    session.viewports['Viewport: 1'].view.fitView()
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        DEFORMED,))
    session.viewports['Viewport: 1'].odbDisplay.display.setValues(plotState=(
        CONTOURS_ON_DEF,))
    session.printOptions.setValues(reduceColors=False)
    # Print SMises plot on deformed shape
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='S', outputPosition=INTEGRATION_POINT, refinement=(
            INVARIANT, 'Mises'), )
    session.printToFile(
        fileName=results_dir + job_name + '/SMises_Deformed' + seed_str,
        format=TIFF, canvasObjects=(session.viewports['Viewport: 1'],))
    # Print displacement plot on deformed shape
    session.viewports['Viewport: 1'].odbDisplay.setPrimaryVariable(
        variableLabel='U', outputPosition=NODAL, refinement=(INVARIANT,
                                                             'Magnitude'), )
    session.printToFile(
        fileName=results_dir + job_name + '/Displacements_Deformed' + seed_str,
        format=TIFF, canvasObjects=(session.viewports['Viewport: 1'],))
    # Print report with SMises and displacements
    odb = session.odbs[home_dir
                       + job_name + seed_str + '.odb']
    session.writeFieldReport(fileName=job_name + seed_str + '.rpt', append=ON,
                             sortItem='Node Label', odb=odb, step=0, frame=1, outputPosition=NODAL,
                             variable=(('U', NODAL, ((COMPONENT, 'U2'), (
                                 COMPONENT, 'U3'),)), ('S', INTEGRATION_POINT,
                                                       ((INVARIANT, 'Mises'),)),), stepFrame=SPECIFY)
    shutil.copy(home_dir + job_name + seed_str + '.rpt', results_dir + job_name + '/')
