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
    try {
      if(input)
      {const gpt_res = await fetch('http://localhost:5000/chat',
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({"history":"[{'role':'system','content':'You are a car assistant. The driver is about to sleep. Wake him/her up and try to hold a conversation'},{'role':'user','content':'I am feeling sleepy. Start a conversation.'}]","new_message":input}), 
              });
      gpt_res.json().then((async obj=>{
        const [path, duration] = await tts(obj);
        
        self.postMessage({"path":path,"message":obj.response,"duration":duration})
      }))}
      else{
        const gpt_res = await fetch('http://localhost:5000/chat',
              {
                method: "POST",
                headers: {
                  "Content-Type": "application/json",
                },
                body: JSON.stringify({"history":"[{'role':'system','content':'You are a car assistant. The driver is about to sleep. Wake him/her up and try to hold a conversation'}]","new_message":"I am feeling sleepy. Start a conversation."}), 
              });
      gpt_res.json().then((async obj=>{
        const [path, duration] = await tts(obj);
        
        self.postMessage({"path":path,"message":obj.response,"duration":duration})
      }))
      }
      
    } catch (error) {
      console.error('Error chat:', error);
    }
    
  }

if(e.data == 'Wake Up') 
  chat();  
else
  chat(e.data)
  
};