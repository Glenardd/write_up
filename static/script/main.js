let panel = document.getElementById('panel');

document.getElementById('burger-btn').addEventListener('click', hide)

if (sessionStorage.getItem('save-panel') === "true") {
    panel.style.display = 'none';    
} 
else if(sessionStorage.getItem('save-panel') === "false"){
    panel.style.display = 'block';
}

//onclick event
function hide(){
    if(panel.style.display == 'none'){
        panel.style.display = 'block';
        sessionStorage.setItem('save-panel', "false");
    }else{
        console.log('hidden')
        panel.style.display = 'none';    
        sessionStorage.setItem('save-panel', "true");
    }
}