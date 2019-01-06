/*
	hollowCylinder() v1.0.0 by robert@cosmicrealms.com from https://github.com/Sembiance/openscad-modules
	Allows you to create a hollow cylinder
	
	Usage
	=====
	Prototype: hollowCylinder(d, h, wallWidth, $fn)
	Arguments:
		-         d = Diamater of the cylinder. Default: 5
		-         h = Height of the cylinder. Default: 10
		- wallWidth = How wide the walls should be. Default: 1
		-       $fn = How smooth you want the cylinder rounding to be. Default: 128
	Change Log
	==========
	2017-01-04: v1.0.0 - Initial Release
*/

// Example code:
/*
hollowCylinder(d=10, h=20);
translate([15, 0, 0]) { hollowCylinder(d=15, h=5, wallWidth=0.1); }
translate([30, 0, 0]) { hollowCylinder(d=10, h=2, wallWidth=4.5); }
*/

module hollowCylinder(d=5, h=10, wallWidth=1, $fn=128)
{
	difference()
	{
		cylinder(d=d, h=h);
		translate([0, 0, -0.1]) { cylinder(d=d-(wallWidth*2), h=h+0.2); }
	}
}

union(){
union(){
hull(){
    hollowCylinder(8,1,0.1,256);
    translate([10,0,0]){
        hollowCylinder(8,1,0.1,256);
    }
}

hull(){
    hollowCylinder(8,1,0.1,256);
    translate([0,10,0]){
        hollowCylinder(8,1,0.1,256);
    }
}
}

translate([-8,-8,0]){
difference(){
    translate([8,8,0]){
    cube([8,8,1]);
}
translate([16,16,0]){
    cylinder(d=10, h=1, $fn=256);
}
}
}
}
