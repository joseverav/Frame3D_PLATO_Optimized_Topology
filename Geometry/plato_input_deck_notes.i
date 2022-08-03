/* Use ParaView to visualize results
Select topology
Use filter -> alphabetical -> iso volume to see full shape
Input scalars = topology
*/

// DEFINE OBJECTIVE
begin objective
   type maximize stiffness
   // type minimize mass stress constraint
   load ids 1 2 //Corresponds to loads active during optimization
   boundary condition ids 1 2
   code plato_analyze
   number processors 1
end objective

// DEFINE BC'S AND LOADS
begin boundary conditions
   fixed displacement nodeset name surface_8 bc id 1
   fixed displacement nodeset name surface_14 bc id 2
   // can also do time-dependent and specified displacement
end boundary conditions

begin loads // traction and pressure loads supported. Everything same, except value
    traction sideset name surface_3 value 0 -15 0 load id 1 // Downward load acting at top of beam
    traction sideset name surface_5 value 0 -113.7 0 load id 1 // Earthquake load acting on side of beam in -z direction
    // Add more lines of code here for more loads. Same concept for BCs
end loads

// DEFINE CONSTRAINTS
begin constraint 
   type volume // can do other ones
   volume fraction .35
end constraint

// DEFINE BLOCK MATERIAL ASSIGNMENTS
begin block 1
   material 1
end block

begin block 2
   material 1
end block

begin block 3
   material 1
end block

// DEFINE MATERIALS
begin material 1 // Steel
   poissons ratio .303
   youngs modulus 29e6
   // density 1e3
end material

// DEFINE OPTIMIZATION PARAMETERS
begin optimization parameters
   number processors 1
   filter radius scale 2.5
   max iterations 50 
   output frequency 1000 
   algorithm oc
   discretization density 
   initial density value .
   // fixed (Number of block to be fixed)
end optimization parameters

begin mesh
   name frame.exo
   // Use mesh IO
end mesh

begin code
   code PlatoMain
   code analyze_MPMD
end code
