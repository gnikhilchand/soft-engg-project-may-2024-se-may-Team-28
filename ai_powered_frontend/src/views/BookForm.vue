<template>
    <div>
      <h2>{{ mode === 'add' ? 'Add New Book' : 'Edit Book' }}</h2>
      <form @submit.prevent="submitForm" calss="search-container">
        <div>
          <label>Title:</label>
          <input type="text" v-model="book.title" required>
        </div>
        <div>
          <label>ISBN:</label>
          <input type="text" v-model="book.isbn" required>
        </div>
        <div>
          <label>Year:</label>
          <input type="number" v-model="book.year" required>
        </div>
        
        <button type="submit" class="button">{{ mode === 'add' ? 'Add Book' : 'Update Book' }}</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    props: ['bookData', 'mode'], 
    data() {
      return {
        book: { ...this.bookData } 
      };
    },
    methods: {
      submitForm() {
        if (this.mode === 'add') {
          // Submit new book data
          fetch('http://localhost:5000/api/books', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.book)
          })
          .then(response => {
            if (response.ok) {
              // Handle success, e.g., show success message or redirect to books list
              console.log('Book added successfully');
            } else {
              console.error('Error adding book:', response.statusText);
            }
          })
          .catch(error => {
            console.error('Error adding book:', error);
          });
        } else if (this.mode === 'edit') {
          // Submit updated book data
          fetch(`http://localhost:5000/api/books/${this.book.id}`, {
            method: 'PUT',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify(this.book)
          })
          .then(response => {
            if (response.ok) {
              // Handle success, e.g., show success message or redirect to books list
              
              alert('Book updated successfully please refresh this page')
            } else {
              console.error('Error updating book:', response.statusText);
            }
          })
          .catch(error => {
            console.error('Error updating book:', error);
          });
        }
      }
    }
  };
  </script>
  <style scoped>
  

 .container {
    width: 400px;
    margin: 0 auto;
  }
  
  h2 {
    font-size: 24px;
    text-align: center;
  }
  
  form {
    background-color: #f2f2f2;
    padding: 20px;
    border-radius: 8px;
  }
  
  label {
    display: block;
    margin-bottom: 5px;
  }
  
  input[type="text"],
  input[type="number"] {
    width: calc(100% - 10px);
    padding: 8px;
    margin-bottom: 15px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }
  
  button {
    background-color: #007bff;
    color: #fff;
    border: none;
    padding: 10px 20px;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
</style>