<template>
  <div id="app">
      
      <router-view />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'App',
  components: {
      
  },
  setup() {
      const router = useRouter();

      // Check user role before loading the application
      const checkUserRole = () => {
          const userString = localStorage.getItem('user');
          if (userString) {
              const user = JSON.parse(userString);
              // Ensure user object has a 'role' property
              if (user && user.role) {
                  // The user is authenticated and has a role
                  return;
              } else {
                  // If user has no role or is not authenticated, redirect to login
                  router.push('/login');
              }
          } else {
              // No user data found, redirect to login
              router.push('/login');
          }
      };

      // Call the function in the `created` lifecycle hook
      checkUserRole();
  },
});
</script>