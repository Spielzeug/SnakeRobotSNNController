difference(){
    
    translate([-0.5,-0.5,0]){
    union() {
translate([-5,-5,0]) {
    cylinder(d=20, h=2, $fn=256);
    translate([-10,0,0]) {
        cube([10,30,2]);
    }
    
    translate([0,-10,0]) {
        cube([30,10,2]);
    }
}
}
}
union() {
translate([-5,-5,0]) {
    cylinder(d=20, h=2, $fn=256);
    translate([-10,0,0]) {
        cube([10,30,2]);
    }
    
    translate([0,-10,0]) {
        cube([30,10,2]);
    }
}
}


}

