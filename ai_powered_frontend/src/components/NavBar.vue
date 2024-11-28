<template>
  <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
          <router-link class="navbar-brand" to="/">AILMS</router-link>
          <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
              aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" id="navbarNav">
              <ul class="navbar-nav">
                  <!-- Routes for User -->
                  <li v-if="userRole === 'User'" class="nav-item">
                      <router-link class="nav-link" to="/explore">Books</router-link>
                  </li>
                  <li v-if="userRole === 'User'" class="nav-item">
                      <router-link class="nav-link" to="/user">Dashboard</router-link>
                  </li>

                  <!-- Routes for Admin -->
                  <li v-if="userRole === 'Admin'" class="nav-item">
                      <router-link class="nav-link" to="/admin">Admin Panel</router-link>
                  </li>

                  <!-- Dropdown for Admin -->
                  <li v-if="userRole === 'Admin'" class="nav-item dropdown">
                      <router-link class="nav-link dropdown-toggle" to="/admin" role="button" data-bs-toggle="dropdown"
                          aria-expanded="false">
                          Utilities 
                      </router-link>
                      <ul class="dropdown-menu">
                          <li><router-link class="dropdown-item" to="/useradmin">Users</router-link></li>
                          <li><router-link class="dropdown-item" to="/explore">Courses</router-link></li>
                          <li><router-link class="dropdown-item" to="/summarizer">Transcript <Summary></Summary></router-link></li>
                      </ul>
                  </li>

                  <!-- Login and Signup if not logged in -->
                  <li v-if="!userRole" class="nav-item">
                      <router-link class="nav-link" to="/login">Login</router-link>
                  </li>
                  <li v-if="!userRole" class="nav-item">
                      <router-link class="nav-link" to="/signup">Signup</router-link>
                  </li>

                  <!-- Logout button -->
                  <li v-if="userRole" class="nav-item">
                      <button class="nav-link btn btn-link" @click="logout">Logout</button>
                  </li>
              </ul>
          </div>
      </div>
  </nav>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'NavBar',
  setup() {
      const router = useRouter();
      const userRole = ref<string | null>(null);

      // Retrieve user role from local storage
      onMounted(() => {
          const userString = localStorage.getItem('user');
          if (userString) {
              const user = JSON.parse(userString);
              // Ensure the user object has a 'role' property
              if (user && user.role) {
                  userRole.value = user.role;
              } else {
                  userRole.value = null;
              }
          } else {
              userRole.value = null;
          }
      });

      // Logout function
      const logout = () => {
          localStorage.removeItem('user'); // Clear local storage
          userRole.value = null; // Set user role to null
          router.push('/login'); // Redirect to the login page
      };

      return {
          userRole,
          logout,
      };
  },
});
</script>

<style scoped lang="scss">
/* Add your component-specific styles here */
</style>
