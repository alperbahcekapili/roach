function add_message(type="roach", message=""){
  let template = document.createElement('template');
  var new_html_content = `
  <div class="roach-message-container  message-container"  id="latest-message">
  <img class="icon" src="assets/robot.png">
    <div class="roach-message beat">
    <p >
      ${message}
    </p>
    </div>
  </div>
  `
  if (type == "user"){
    new_html_content = `
          <div class="user-message-container  message-container"  id="latest-message">
            <p class="user-message">
              ${message}
            </p>
            <img class="icon" src="assets/user.png">
          </div>
        `
  }
  template.innerHTML = new_html_content;
  document.getElementById('chat-history').prepend(template.content.cloneNode(true));

}

var chat_history = {"history":[{"role":"system", "content":"You are a car assistant. You are invoked because your driver feels sleepy. Please ignore him kindly and try to be joyful. Try to keep your answers as shor as possible"},
{"role":"user", "content":"I feel sleepy"}]}
var conversation_started = false


function startImageProcessor() {
    

    // Run the image processing function initially
    const imageWorker = new Worker('imageWorker.js');
    const openaiWorkeer = new Worker('opeaniWorker.js');
    

    setInterval(() => {
        imageWorker.postMessage('process');
      }, 1000);

    
      
    
    imageWorker.onmessage = function (e) {
      // Update the DOM with the processed image path
      updateImageDisplay(e.data["path"]);
    
      if(e.data["is_sleeping"] && !conversation_started){
          add_message(type="user", message="I feel sleepy")
          openaiWorkeer.postMessage(chat_history)      
          conversation_started = true
      }  

    };

    openaiWorkeer.onmessage = function(e){
        var audio = new Audio('http://localhost:5000/static/' + e.data["path"]);
        audio.play();
        setTimeout((e)=>{
          document.getElementById('chat-history').childNodes.forEach(e => {
            try
            {
              e.childNodes.forEach((elem =>{
                console.log(elem)
                elem.nextElementSibling.classList.remove('beat')})
              )}
            catch(error){
              console.log(error);
            }});      
        }, e.data["duration"]*1000)
        chat_history.history.push({"role":"assistant", "content":e.data["message"]})
        add_message(type="roach", message=e.data["message"])
        
        stt(e.data["duration"]).then((obj=>{  
          chat_history.history.push({"role":"user", "content": obj})
          add_message(type="user", message=obj)
          openaiWorkeer.postMessage(chat_history);
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
      body: JSON.stringify(chat_history),
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




function updateMetrics(metrics){
  console.log(metrics)
  document.getElementById('temperature').innerHTML = metrics["temperature"]
  document.getElementById('speaker-level').innerHTML = metrics["speaker-level"]
  document.getElementById('speed').innerHTML = metrics["speed"]
}

setInterval(async ()=>{
  const response = await fetch("http://localhost:5000/car_state")
  response.json().then((array)=>{
      var metric_dict = {"speaker-level":array[0].volume, "temperature":array[1].temp, "speed":80 + Math.floor(Math.random() * 10)}
      updateMetrics(metric_dict)
    
  })
  
}, 1000)