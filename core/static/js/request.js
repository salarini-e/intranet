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
