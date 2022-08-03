// Gmsh project created on Tue Dec 08 13:16:43 2020
SetFactory("OpenCASCADE");

//+
Point(1) = {0, 7.95, 0, 1};
//+
Point(2) = {0, -127.95, 0, 1};
//+
Point(3) = {0, -127.95, 15.9, 1};
//+
Point(4) = {0, -7.95, 15.9, 1};
//+
Point(5) = {0, -7.95, 164.1, 1};
//+
Point(6) = {0, -127.95, 164.1, 1};
//+
Point(7) = {0, -127.95, 180, 1};
//+
Point(8) = {0, -7.95, 180, 1};
//+
Point(9) = {0, 7.95, 180, 1};

//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 5};
//+
Line(5) = {5, 6};
//+
Line(6) = {6, 7};
//+
Line(7) = {7, 8};
//+
Line(8) = {8, 9};
//+
Line(9) = {9, 1};

//+
Curve Loop(1) = {1, 2, 3, 4, 5, 6, 7, 8, 9};
//+
Plane Surface(1) = {1};

//+
Extrude {5.53, 0, 0} {
  Curve{1}; Curve{2}; Curve{3}; Curve{4}; Curve{5}; Curve{6}; Curve{7}; Curve{8}; Curve{9}; Surface{1};
}
