
/* eslint-disable */
<template>
    <div>

    <NavBar/>
    <div class="signup-container">
      <div class="signup-form">
        <h2>Sign Up</h2>
        <form @submit.prevent="signup">
          <div class="input-group">
            <input type="text" id="username" v-model="username" placeholder="Username" required />
          </div>
          <div class="input-group">
            <input type="email" id="email" v-model="email" placeholder="Email" required />
          </div>
          <div class="input-group">
            <input type="password" id="password" v-model="password" placeholder="Password" required />
          </div>
          <div class="input-group">
            <select v-model="role">
              <option value="" disabled>Select Role</option>
              <option>User</option>
            </select>
          </div>
          
          

          <button type="submit" class="signup-button">Sign Up</button>
        </form>
      </div>
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
    name: 'HomePage',
  components: {
    NavBar,
    
  },
    data() {
      return {
        username: '',
        email: '',
        password: '',
        role: 'User',
        message: '', // For success or error messages
        messageType: ''
      };
    },
     methods: {
    async signup() {
      const userData = {
        username: this.username,
        email: this.email,
        password: this.password,
        role: this.role,
        membership_type: this.membershipType
        
    };
        axios.post('http://127.0.0.1:8080/auth/signup', userData)
        .then(() => { 
          this.setMessage('User Created successfully!', 'success');

          this.resetForm('signup');
          this.$router.push('/login')
        })
          .catch(error => {
            this.setMessage('Failed to create user. ' + (error.response?.data.message || ''), 'error');
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
      this.username = '';
      this.email = '';
      this.password = '';
      this.role = '';
    }
},
watch: {

}
});
</script>

  <style scoped>
.signup-container {
  max-width: 400px; /* Adjusted size to match the form */
  margin: 50px auto;
  padding: 20px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.15);
  border-radius: 15px;
  background-color: #fff;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: fadeIn 1s ease, float 3s ease-in-out infinite;
}



/* @keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-20px); }
} */

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
  
  .signup-button {
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
  
  .signup-button:hover {
    background-color: #45a049;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
  }
  .signup-button:active {
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