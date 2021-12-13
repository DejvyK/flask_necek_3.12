async function check_position(){
    let user_id;

    const res = await fetch(
        `/api/check_position`,{
            method: 'GET',
            body: JSON.stringify(user_id),
            headers: {"Content-type" : "application/json; charset=UTF-8"}
        }
    )

    .then(res => res.json)
    .then(json => console.log(json))
    .catch(err => console.log(err))
}


const clock = new THREE.Clock()
let clocking = function(){
    let curr_time = clock.getElapsedTime()
    
    if (curr_time < 6 && curr_time > 5 ){
        // console.log(curr_time)
        clock.start()
        check_position(

        )

    }
    
    requestAnimationFrame(clocking)
}
clocking();
