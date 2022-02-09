const position = document.querySelector('#processing_p')

if (position){
    const user_id = position.dataset.user_id
    const queue_id = position.dataset.queue_id
    
    async function check_position(){
        var res = await fetch
        (`/api/check_processing/${queue_id}`)


        data = await res.json();
        
        position.innerHTML = data['position']
    }
    
    
    const clock = new THREE.Clock()
    let clocking = function(){
        let curr_time = clock.getElapsedTime()
        
        if (curr_time < 6 && curr_time > 5 ){
            clock.start()
            check_position()
        }
        
        requestAnimationFrame(clocking)
    }
    clocking();
}
