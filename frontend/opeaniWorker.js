// imageWorker.js
self.onmessage = async function (e) {
    //   try {
    //     const response = await fetch('http://localhost:5000/process_image'); // Adjust the URL accordingly
    //     const result = await response.json();
    //     self.postMessage("http://localhost:5000/static/" + result.processed_image_path);
    //   } catch (error) {
    //     console.error('Error processing image:', error);
    //   }

  async function tts(obj){
    
    try{
        
        const response =  await fetch('http://localhost:5000/tts',
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(obj),
        });
        
        return response.json().then((obj=>{
          return [obj.sound_file_path, obj.duration]
        })) 
    }
    catch (error) {
    console.error('Error tts:', error);
    }
  }  
  async function chat(input){
    // input {history, new_message}
    try {
      if(input)
      {
        console.log(JSON.stringify(input))
        const temp_history = input['history']
        const gpt_res = await fetch('http://localhost:5000/chat',
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({"history":temp_history}) 
              });
        gpt_res.json().then((async obj=>{
          const [path, duration] = await tts(obj);
          // ai's response
          self.postMessage({"path":path,"message":obj.response,"duration":duration})
        }))}
      
    } catch (error) {
      console.error('Error chat:', error);
    }
    
  }


chat(e.data)
  
};