<template>
    <div>

    <NavBar/>
    <div class="container">
      <div class="tabs">
        <div :class="{'tab': true, 'active': activeTab === 'author'}" @click="setActiveTab('author')">Author</div>
        <div :class="{'tab': true, 'active': activeTab === 'publisher'}" @click="setActiveTab('publisher')">Publisher</div>
        <div :class="{'tab': true, 'active': activeTab === 'category'}" @click="setActiveTab('category')">Category</div>
      </div>
  
      <div class="form-container">
        <form v-if="activeTab === 'author'" @submit.prevent="addAuthor">
          <input type="text" v-model="author.name" placeholder="Author Name">
          <textarea v-model="author.biography" placeholder="Biography"></textarea>
          <button type="submit">Add Author</button>
        </form>
  
        <form v-if="activeTab === 'publisher'" @submit.prevent="addPublisher">
          <input type="text" v-model="publisher.name" placeholder="Publisher Name">
          <input type="text" v-model="publisher.address" placeholder="Address">
          <button type="submit">Add Publisher</button>
        </form>
  
        <form v-if="activeTab === 'category'" @submit.prevent="addCategory">
          <input type="text" v-model="category.name" placeholder="Category Name">
          <textarea v-model="category.description" placeholder="Description"></textarea>
          <button type="submit">Add Category</button>
        </form>
      </div>
      <div v-if="message" :class="['message-widget', messageType]">
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
        activeTab: 'author',
        author: {
          name: '',
          biography: ''
        },
        publisher: {
          name: '',
          address: ''
        },
        category: {
          name: '',
          description: ''
        },
        message: '', // For success or error messages
        messageType: '' // 'success' or 'error'
      };
    },
    methods: {
      setActiveTab(tab) {
        this.activeTab = tab;
        this.clearMessages();
      },
      isValidInput(input) {
      return Object.values(input).every(value => value.trim() !== '');
    },
      addAuthor() {
        if (!this.isValidInput(this.author)) {
        this.setMessage('Author fields cannot be empty.', 'error');
        return;
      }
        axios.post('http://localhost:5000/api/authors', this.author)
          .then(() => {  
            this.setMessage('Author added successfully!', 'success');
            this.resetForm('author');
          })
          .catch(error => {
            this.setMessage('Failed to add author. ' + (error.response?.data.message || ''), 'error');
          });
      },
      addPublisher() {
        if (!this.isValidInput(this.publisher)) {
        this.setMessage('Publisher fields cannot be empty.', 'error');
        return;
      }
        axios.post('http://localhost:5000/api/publishers', this.publisher)
          .then(() => {  
            this.setMessage('Publisher added successfully!', 'success');
            this.resetForm('publisher');
          })
          .catch(error => {
            this.setMessage('Failed to add publisher. ' + (error.response?.data.message || ''), 'error');
          });
      },
      addCategory() {
        if (!this.isValidInput(this.category)) {
        this.setMessage('Category fields cannot be empty.', 'error');
        return;
      }
        axios.post('http://localhost:5000/api/categories', this.category)
          .then(() => {  
            this.setMessage('Category added successfully!', 'success');
            this.resetForm('category');
          })
          .catch(error => {
            this.setMessage('Failed to add category. ' + (error.response?.data.message || ''), 'error');
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
      resetForm(formType) {
        if (formType === 'author') {
          this.author.name = '';
          this.author.biography = '';
        } else if (formType === 'publisher') {
          this.publisher.name = '';
          this.publisher.address = '';
        } else if (formType === 'category') {
          this.category.name = '';
          this.category.description = '';
        }
      }
    }
  });
  </script>
  
  <style scoped>
.container {
  max-width: 600px;
  margin: 100px auto;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border-radius: 15px;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: fadeIn 1s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

/* .container:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 36px rgba(0, 0, 0, 0.2);
} */
  
.tabs {
display: flex;
justify-content: center;
margin-bottom: 20px;
}

.tab {
padding: 12px 24px;
cursor: pointer;
font-size: 16px;
color: #555;
transition: all 0.3s ease;
border-radius: 6px;
margin: 0 8px;
background: linear-gradient(45deg, #f9f9f9, #e2e2e2);
box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.tab:hover {
background: linear-gradient(45deg, #e2e2e2, #d5d5d5);
}

  .tab.active {
    color: #fff;
    background: linear-gradient(45deg, #007bff, #0056b3);
    box-shadow: none;
  }
  .form-container {
    animation: fadeIn 0.5s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
  }

  form {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  
  button {
  background-color: #4CAF50;
  color: white;
  padding: 15px 25px;
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