function startImageProcessor() {
    // Run the image processing function initially
    const imageWorker = new Worker('imageWorker.js');
    const openaiWorkeer = new Worker('opeaniWorker.js');

    setInterval(() => {
        console.log("iamge worker triggered")
        imageWorker.postMessage('process');
      }, 50);

    console.log("Here")
    setInterval(() => {
        console.log("opeani worker triggered")
        openaiWorkeer.postMessage('New message');
    }, 800);



    imageWorker.onmessage = function (e) {
    // Update the DOM with the processed image path
    updateImageDisplay(e.data);
    };

    openaiWorkeer.onmessage = function(e){
        new_p = document.createElement("p");
        new_p.appendChild(document.createTextNode("Hi there and greetings!"))
        document.getElementById('chat-history').appendChild(
            new_p
        )
    }

  
  }

  function updateImageDisplay(imagePath) {
    // Update the DOM with the processed image path
    console.log(imagePath)
    var img=new Image();
    img.src=imagePath;
    document.getElementById('imageDisplay').src =  imagePath

  }


async function tts(){
  try {
    data = {"message":"Selam naber"};
    const response =  await fetch('http://localhost:5000/tts',
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data), // body data type must match "Content-Type" header
    });

    response.json().then((obj=>{
      var audio = new Audio('http://localhost:5000/static/' + obj.sound_file_path);
      audio.play();
    }))
    
      
    
    
  } catch (error) {
    console.error('Error processing image:', error);
  }
}

async function stt(){
  try {
    const response =  await fetch('http://127.0.0.1:5000/record',
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(""), // body data type must match "Content-Type" header
    });

    response.json().then((obj=>{
      console.log(obj.response)
    }))
    
      
    
    
  } catch (error) {
    console.error('Error processing image:', error);
  }
}

