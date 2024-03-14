function postRequest(url, form) {
    return fetch(url, {
      method: 'POST',
      body: form,
    })
    .then(response => {
      if (!response.ok) {
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .catch(error => {
      console.error('There was a problem with the fetch operation:', error);
      throw error; 
    });
  }


function getRequest(url, callback) {
    var xhr = new XMLHttpRequest();
    
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) { 
            callback(xhr.responseText);
        }
    };

    xhr.open("GET", url, true); 
    xhr.send(); 
}