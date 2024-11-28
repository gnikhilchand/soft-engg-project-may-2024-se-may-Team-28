<template>
  <div>

  <NavBar/>
    <div class="book-form">

    <!-- <div v-if="showSuccess" class="message success-message">
      {{ successMessage }}
    </div>

    <div v-if="showError" class="message error-message">
      {{ errorMessage }}
    </div> -->
        
      <form @submit.prevent="submitForm">
        <div class="input-group">
          
          <input type="text" id="title" v-model="book.title" placeholder="Title" required>
        </div>
  
        <div class="input-group">
          
          <input type="text" id="isbn" v-model="book.isbn"  placeholder="Unique Identitification Number" required>
        </div>
  
        <div class="input-group">
          
          <input type="number" id="year" v-model="book.year" placeholder="Year" required>
        </div>
  
        <div class="input-group">
      <label for="author">Author</label>
      <select id="author" v-model="book.author_id" required>
        <option disabled value="">Please select one</option>
        <option v-for="author in authors" :value="author.id" :key="author.id">
          {{ author.name }}
        </option>
      </select>
    </div>

    <div class="input-group">
      <label for="publisher">Publisher</label>
      <select id="publisher" v-model="book.publisher_id">
        <option disabled value="">Please select one</option>
        <option v-for="publisher in publishers" :value="publisher.id" :key="publisher.id">
          {{ publisher.name }}
        </option>
      </select>
    </div>

    <div class="input-group">
      <label for="category">Category</label>
      <select id="category" v-model="book.category_id">
        <option disabled value="">Please select one</option>
        <option v-for="category in categories" :value="category.id" :key="category.id">
          {{ category.name }}
        </option>
      </select>
    </div>
    <div class="input-group">
        <label for="pdf">PDF File</label>
        <input type="file" id="pdf" ref="file" @change="handleFileUpload" accept=".pdf" required>
        <span v-if="book.file" class="file-selected">File selected: {{ book.file.name }}</span>
      </div>
  
        <button type="submit">Submit</button>
      </form>
     
      <div  v-if="message" :class="['message-widget', messageType]">
  {{ message }}
</div>
    </div>
  </div>
  </template>
  
<script>
  import axios from 'axios';
  import { defineComponent } from 'vue';
import NavBar from '../components/NavBar.vue';
  
export default defineComponent({
    components: {
    NavBar,
  },
  

    data() {
      return {
        book: {
          title: '',
          isbn: '',
          year: null,
          author_id: '',
          publisher_id: '',
          category_id: ''
        },
        authors: [],
        publishers: [],
        categories: [],
        message: '', // For success or error messages
        messageType: ''
      };
    },
    methods: {
      fetchAuthors() {
        axios.get('http://localhost:5000/api/authors')
          .then(response => {
            this.authors = response.data;
          })
          .catch(error => {
            console.error("Error fetching authors:", error);
          });
      },
      fetchPublishers() {
        axios.get('http://localhost:5000/api/publishers')
          .then(response => {
            this.publishers = response.data;
          })
          .catch(error => {
            console.error("Error fetching publishers:", error);
          });
      },
      fetchCategories() {
        axios.get('http://localhost:5000/api/categories')
          .then(response => {
            this.categories = response.data;
          })
          .catch(error => {
            console.error("Error fetching categories:", error);
          });
      },
      handleFileUpload() {
      this.book.file = this.$refs.file.files[0];
    },
    //   submitForm() {
    //     axios.post('http://localhost:5000/api/add-book', this.book)
    //     .then(() => {  
    //   this.setMessage('Book added successfully', 'success');
    //   this.resetForm('book');
      
    // })
    // .catch(error => {
    //   this.setMessage("Something went wrong: " + (error.response?.data.message || ''), 'error');
    // });
    //   },
    submitForm() {
      let formData = new FormData();
      
      // Append book data to formData
      Object.keys(this.book).forEach(key => formData.append(key, this.book[key]));

      
      axios.post('http://localhost:5000/api/add-book', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(() => {  
        this.setMessage('Book added successfully', 'success');
        this.resetForm();
      })
      .catch(error => {
        this.setMessage("Something went wrong: " + (error.response?.data.message || ''), 'error');
      });
    },
      setMessage(msg, type) {
    this.message = msg;
    this.messageType = type;
    this.$nextTick(() => {
      // Ensure the DOM has updated before adding the 'show' class
      document.querySelector('.message-widget').classList.add('show');
    });
    setTimeout(() => {
      this.clearMessages();
    }, 5000);
  },

  clearMessages() {
    const widget = document.querySelector('.message-widget');
    if (widget) {
      widget.classList.remove('show');
    }
    this.message = '';
    this.messageType = '';
  },
  resetForm() {
  this.book = {
    title: '',
    isbn: '',
    year: null,
    author_id: '',
    publisher_id: '',
    category_id: '',
    file: null
  };
  if (this.$refs.file) {
    this.$refs.file.value = '';
  }
},
    
  },
  mounted() {
      console.log("Mounted Hook Called");
      this.fetchAuthors();
      this.fetchPublishers();
      this.fetchCategories();
    }
});
  </script>
  
  <style scoped>
  .book-form {
    max-width: 600px; /* Adjusted size to match the form */
  margin: 50px auto;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border-radius: 15px;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: fadeIn 1s ease, float 3s ease-in-out infinite;
}

  
  

form {
  display: flex;
  flex-direction: column;
  gap: 5px;
  animation: slideIn 0.5s ease-out;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.signup-form {
  animation: fadeIn 0.5s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
  }


.signup-form h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
  transition: color 0.3s ease;
}
input, textarea {
  padding: 15px;
  border: 2px solid transparent;
  border-radius: 8px;
  transition: all 0.3s ease-in-out;
  background-color: #f8f9fa;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

input:focus, textarea:focus {
  outline: none;
  border-color: #007bff;
  background-color: #ffffff;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.15);
}

input::placeholder, textarea::placeholder {
  color: #6c757d;
  transition: color 0.3s ease-in-out;
}

input:focus::placeholder, textarea:focus::placeholder {
  color: #007bff;
}

  


.input-group {
  margin-bottom: 15px;
  position: relative;
  transition: transform 0.3s ease;
}

.input-group input:focus, .input-group select:focus {
  outline: none;
  border-color: #007bff;
}

.input-group input,
.input-group select {
width: 100%;
padding: 12px;
border: 1px solid #ddd;
border-radius: 4px;
box-sizing: border-box;
transition: border-color 0.3s ease;
}

.input-group input:focus, .input-group select:focus {
border-color: #007bff;
box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

.input-group label {
display: block;
margin-bottom: 5px;
color: #666;
transition: color 0.3s ease;
}

.input-group:hover label {
color: #007bff;
}
input[type="file"] {
  width: 100%;
  padding: 10px 15px;
  border-radius: 8px;
  border: 2px solid transparent;
  background-color: #f8f9fa;
  transition: border-color 0.3s, box-shadow 0.3s;
  outline: none;
}

input[type="file"]::file-selector-button {
  padding: 10px 15px;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  border: none;
  transition: background-color 0.3s;
}

input[type="file"]::file-selector-button:hover {
  background-color: darken(#007bff, 10%);
  cursor: pointer;
}

input[type="file"]:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 3px rgba(0, 123, 255, 0.25);
}

input[type="file"]:hover {
  border-color: #007bff;
}

/* Styles for file selected message */
.file-selected {
  position: absolute;
  top: 100%;
  left: 0;
  width: 100%;
  padding: 5px 0;
  margin-top: 2px; /* Added margin for space between the input and the message */
  font-size: 14px;
  color: #28a745;
  text-align: center;
  animation: fadeIn 0.3s;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

  
button {
    background-color: #4CAF50;
  color: white;
  padding: 15px 25px;
  margin-top: 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: transform 0.3s ease, background-color 0.3s ease;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.5px;
  }
  
 button:hover {
    background-color: #45a049;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
  }
  button:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.message-widget {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%) translateY(50px); /* Center horizontally and start below the view */
  padding: 15px 25px;
  border-radius: 10px;
  color: white;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
  transition: transform 0.5s ease, opacity 0.5s ease;
  opacity: 0;
  z-index: 1000; /* Ensure it's above other elements */
  background-color: #333; /* Default background color */
  width: auto;
  max-width: 80%; /* Max width */
  min-width: 300px; /* Minimum width */
  text-align: center;
  font-size: 16px;
}

.message-widget.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0); /* Slide up into view */
}

.message-widget.success {
  background-color: #28a745; /* Green for success messages */
}

.message-widget.error {
  background-color: #dc3545; /* Red for error messages */
}

/* Optional: Add keyframe animation for a bounce effect */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {transform: translateX(-50%) translateY(0);}
  40% {transform: translateX(-50%) translateY(-20px);}
  60% {transform: translateX(-50%) translateY(-10px);}
}

.message-widget.show {
  animation: bounce 1s ease;
}

  </style>