document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filter-form');
    const bookRequestsContainer = document.getElementById('book-requests');
  
    filterForm.addEventListener('submit', function(event) {
      event.preventDefault();
  
      const genre = document.getElementById('genre').value;
      const title = document.getElementById('title').value;
  
      fetch(`/api/findRequests?genre=${genre}&title=${title}`)
        .then(response => response.json())
        .then(data => {
          bookRequestsContainer.innerHTML = '';
  
          data.forEach(book => {
            const bookElement = createBookElement(book);
            bookRequestsContainer.appendChild(bookElement);
          });
        });
    });
  
    function createBookElement(book) {
      // Create and populate the book request element
      const bookElement = document.createElement('div');
      bookElement.classList.add('book-request');
  
      const titleElement = document.createElement('h3');
      titleElement.textContent = book.title;
      bookElement.appendChild(titleElement);
  
      const authorElement = document.createElement('p');
      authorElement.textContent = `Author: ${book.author}`;
      bookElement.appendChild(authorElement);
  
      const genreElement = document.createElement('p');
      genreElement.textContent = `Genre: ${book.genre}`;
      bookElement.appendChild(genreElement);
  
      const synopsisElement = document.createElement('p');
      synopsisElement.textContent = `Synopsis: ${book.synopsis}`;
      bookElement.appendChild(synopsisElement);
  
      const commentsElement = document.createElement('div');
      commentsElement.classList.add('comments');
      const commentsTitle = document.createElement('h4');
      commentsTitle.textContent = 'Comments:';
      commentsElement.appendChild(commentsTitle);
      bookElement.appendChild(commentsElement);
  
      const commentBoxElement = document.createElement('div');
      commentBoxElement.classList.add('comment-box');
      const commentForm = document.createElement('form');
      commentForm.action = `/book/${book.id}/comment`;
      commentForm.method = 'post';
      const commentTextArea = document.createElement('textarea');
      commentTextArea.name = 'text';
      commentTextArea.required = true;
      commentForm.appendChild(commentTextArea);
      const commentSubmitButton = document.createElement('button');
      commentSubmitButton.type = 'submit';
      commentSubmitButton.textContent = 'Add Comment';
      commentForm.appendChild(commentSubmitButton);
      commentBoxElement.appendChild(commentForm);
      bookElement.appendChild(commentBoxElement);
  
      return bookElement;
    }
  });