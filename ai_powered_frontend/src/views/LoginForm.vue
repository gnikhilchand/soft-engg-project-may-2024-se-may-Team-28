<template>
    <div>
      <NavBar/>
  
      <div class="login-container">
        <div class="login-form">
          <h2>Login</h2>
          <form @submit.prevent="attemptLogin">
            <div class="input-group">
              <input type="text" id="username" v-model="username" placeholder="Username" required />
            </div>
            <div class="input-group">
              <input type="password" id="password" v-model="password" placeholder="Password" required />
            </div>
            <button type="submit" class="login-button">Login</button>
            <button type="button" class="login-button" @click="redirectToSignup">Sign Up</button>
            <a href="#" @click.prevent="showForgotPassword" class="forgot-password">Forgot Password?</a>
          </form>
        </div>
        <div v-if="showWidget" :class="['widget', messageType]">
          {{ message }}
        </div>
      </div>
      <div v-if="forgotPasswordModal" class="modal">
      <div class="modal-content">
        <h3>Forgot Password</h3>
        <form @submit.prevent="sendResetEmail">
          <div class="input-group">
            <input type="email" v-model="resetEmail" placeholder="Enter your email" required />
          </div>
          <button type="submit" class="login-button">Send Reset Email</button>
          <button type="button" class="login-button cancel" @click="closeForgotPasswordModal">Cancel</button>
        </form>
      </div>
    </div>
    </div>
  </template>
  
  <script >
  import axios  from 'axios';
  import { defineComponent } from 'vue';
  import NavBar from '../components/NavBar.vue';
  export default defineComponent({
    components: {
      NavBar,
    },
    data() {
      return {
        username: '',
        password: '',
        message: '', // For success or error messages
        messageType: '',
        showWidget: false,
        forgotPasswordModal: false,
      resetEmail: '',
        
      };
    },
    
    methods: {
      async attemptLogin() {
      try {
        const response = await axios.post('http://127.0.0.1:8080/auth/login', {
            username: this.username,  // Assuming you are using email to login
            password: this.password,
        });

        if (response.data.user) {
            // Storing user information in local storage
            localStorage.setItem("user", JSON.stringify(response.data.user));
            if (response.data.user.role === "Admin") {
                this.$router.push('/admin');
            } else {
                this.$router.push('/user');
            }
        } else {
            console.error('Invalid login response', response);
        }
    } catch (error) {
        this.userRegistered = false;
        console.error('Login request failed', error);
    }
},
      setMessage(msg, type) {
        this.message = msg;
        this.messageType = type;
        this.showWidget = true;
        setTimeout(() => {
          this.clearMessages();
        }, 5000);
      },
      clearMessages() {
        this.message = '';
        this.messageType = '';
        this.showWidget = false;
      },
      redirectToSignup() {
      this.$router.push('/signup');
    },
    showForgotPassword() {
      this.forgotPasswordModal = true;
    },
    closeForgotPasswordModal() {
      this.forgotPasswordModal = false;
      this.resetEmail = '';
    },
    async sendResetEmail() {
      try {
        const response = await axios.post('https://7ac9-2401-4900-44c1-f24-e974-34fa-d08a-dda6.ngrok-free.app/auth/reset_password', {
          email: this.resetEmail,
        });
        this.setMessage(response.data.message, 'success');
        this.closeForgotPasswordModal();
      } catch (error) {
        this.setMessage(error.response?.data?.message || 'Error sending reset email', 'error');
      }
    },

    
    },
    });
  </script>
  


<style scoped>
.login-container {
    max-width: 400px; /* Adjusted size to match the form */
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


.login-form {
    animation: fadeIn 0.5s ease-in-out;
  }

  @keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to { opacity: 1; transform: translateY(0); }
  }

.login-form h2 {
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
  

.login-button {
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

.login-button:hover {
    background-color: #45a049;
  transform: translateY(-3px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.25);
  
}

.login-button:active {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.widget {
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
/* Different background color for error messages */
.widget.show {
  opacity: 1;
  transform: translateX(-50%) translateY(0); /* Slide up into view */
}

.widget.success {
  background-color: #28a745; /* Green for success messages */
}

.widget.error {
  background-color: #dc3545; /* Red for error messages */
}

/* Optional: Add keyframe animation for a bounce effect */
@keyframes bounce {
  0%, 20%, 50%, 80%, 100% {transform: translateX(-50%) translateY(0);}
  40% {transform: translateX(-50%) translateY(-20px);}
  60% {transform: translateX(-50%) translateY(-10px);}
}

.widget.show {
  animation: bounce 1s ease;
}

/* Responsive design */
@media (max-width: 600px) {
  .login-form {
    width: 90%;
  }
}

.forgot-password {
  display: block;
  text-align: center;
  margin-top: 15px;
  color: #007bff;
  text-decoration: none;
}

.forgot-password:hover {
  text-decoration: underline;
}

.modal {
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0,0,0,0.4);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: #fefefe;
  padding: 20px;
  border-radius: 5px;
  width: 300px;
}

.modal-content h3 {
  margin-top: 0;
}

.modal-content .input-group {
  margin-bottom: 15px;
}

.modal-content .login-button {
  margin-top: 10px;
}
</style>