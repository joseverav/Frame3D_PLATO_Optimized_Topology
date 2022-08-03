//+
Point(1) = {0, 0, 0, 0.3};
//+
Point(2) = {30, 0, 0, 0.3};
//+
Point(3) = {30, 4, 0, 0.3};
//+
Point(4) = {30.25, 4.5, 0, 0.3};
//+
Point(5) = {30.25, 5.5, 0, 0.3};
//+
Point(6) = {30, 6, 0, 0.3};
//+
Point(7) = {30, 10, 0, 0.3};
//+
Point(8) = {0, 10, 0, 0.3};
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
Line(8) = {8, 1};
//+
Line Loop(1) = {7, 8, 1, 2, 3, 4, 5, 6};
//+
Plane Surface(1) = {1};
//+
Extrude {0, 0, 10} {
  Line{7}; Surface{1}; Line{8}; Line{1}; Line{2}; Line{3}; Line{4}; Line{5}; Line{6}; 
}
//+
Hide "*";
//+
Show {
  Point{9}; Point{10}; Point{16}; Point{20}; Point{24}; Point{28}; Point{32}; Point{36}; Curve{9}; Curve{15}; Curve{16}; Curve{17}; Curve{18}; Curve{19}; Curve{20}; Curve{21}; Surface{54}; 
}
//+
Show "*";
