// imageWorker.js
self.onmessage = async function (e) {
    if (e.data === 'process') {
      try {
        const response = await fetch('http://localhost:5000/process_image'); // Adjust the URL accordingly
        const result = await response.json();
        //self.postMessage("http://localhost:5000/static/" + result.processed_image_path);
        // path = "http://localhost:5000/static/tmptopch8u6.png"
        // is_sleeping = false
        self.postMessage({"path":"http://localhost:5000/static/" + result.processed_image_path,"is_sleeping":result.is_sleeping});
      } catch (error) {
        console.error('Error processing image:', error);
      }
    }
  };