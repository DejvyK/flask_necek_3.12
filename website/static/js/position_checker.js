const clock = new THREE.Clock()
let clocking = function(){
    let curr_time = clock.getElapsedTime()
    
    if (curr_time < 6 && curr_time > 5 ){
        console.log(curr_time)
        clock.start()
    }
    
    requestAnimationFrame(clocking)
}
clocking();
