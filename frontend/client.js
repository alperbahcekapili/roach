function startImageProcessor() {
    // Run the image processing function initially
    const imageWorker = new Worker('imageWorker.js');
    const openaiWorkeer = new Worker('opeaniWorker.js');
    

    setInterval(() => {
        imageWorker.postMessage('process');
      }, 50);

    /*setInterval(() => {
        openaiWorkeer.postMessage('New message');
    }, 800);*/

    imageWorker.onmessage = function (e) {
    // Update the DOM with the processed image path

    if(e.data["is_sleeping"]){
        openaiWorkeer.postMessage('Wake Up')
        
    }  
    
    updateImageDisplay(e.data["path"]);
    
    };
    openaiWorkeer.postMessage('Wake Up')

    openaiWorkeer.onmessage = function(e){
        var audio = new Audio('http://localhost:5000/static/' + e.data["path"]);
        audio.play();
        new_p = document.createElement("p");
        new_p.appendChild(document.createTextNode(e.data["message"]))
        document.getElementById('chat-history').appendChild(
            new_p
        )
        
        stt(e.data["duration"]).then((async obj=>{
          console.log(obj);
          openaiWorkeer.postMessage(obj);
          
        }));
        
    }

  
  }

function updateImageDisplay(imagePath) {
  // Update the DOM with the processed image path
  console.log(imagePath)
  var img=new Image();
  img.src=imagePath;
  document.getElementById('imageDisplay').src =  imagePath

}





function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
async function stt(i){
  await sleep(i * 1000);
  try {
    const response =  await fetch('http://127.0.0.1:5000/record',
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(""),
    });

    return response.json().then((obj=>{
      console.log(obj.response)
      return obj.response
    }))    
  } 
  catch (error) {
    console.error('Error processing image:', error);
  }
}

