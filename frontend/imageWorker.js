// imageWorker.js
self.onmessage = async function (e) {
    if (e.data === 'process') {
      try {
        const response = await fetch('http://localhost:5000/process_image'); // Adjust the URL accordingly
        const result = await response.json();
        self.postMessage("http://localhost:5000/static/" + result.processed_image_path);
      } catch (error) {
        console.error('Error processing image:', error);
      }
    }
  };