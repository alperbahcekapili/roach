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
        console.log("Hi")
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