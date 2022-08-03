begin objective
   type maximize stiffness
   load ids 1 2
   boundary condition ids 1 2
   code plato_analyze
   number processors 1
end objective

begin boundary conditions
   fixed displacement nodeset name surface_2 bc id 1
   fixed displacement nodeset name surface_6 bc id 2
end boundary conditions

begin loads
    traction sideset name surface_9 value 0 -15 0 load id 1
    traction sideset name surface_8 value 0 0 -113.7 load id 2
end loads

begin constraint 
   type volume
   volume fraction .35
end constraint

begin block 1
   material 1
end block

begin material 1
   poissons ratio .303
   youngs modulus 29e6
end material

begin optimization parameters
   number processors 1
   filter radius scale 2.5
   max iterations 50 
   output frequency 1000 
   algorithm oc
   discretization density 
   initial density value .5
end optimization parameters

begin mesh
   name frame.exo
end mesh

begin code
   code PlatoMain
   code analyze_MPMD
end code
