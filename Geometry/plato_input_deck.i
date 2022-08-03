begin objective
   type maximize stiffness
   load ids 1
   boundary condition ids 1 2
   code plato_analyze
   number processors 1
end objective

begin boundary conditions
   fixed displacement sideset name sideset_1 bc id 1
   fixed displacement sideset name sideset_2 bc id 2
end boundary conditions

begin loads
    traction sideset name sideset_4 value 0 -15 0 load id 1
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
   max iterations 100
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