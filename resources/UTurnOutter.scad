difference(){
    
scale([1.05,1,1]){
cylinder(d=20, h=2, $fn=256);
translate([-10,0,0]){
    cube([20,30,2]);
}
}
translate([0,1,0]){
cylinder(d=20, h=2, $fn=256);
translate([-10,0,0]){
    cube([20,30,2]);
}
}
}