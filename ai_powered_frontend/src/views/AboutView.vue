<template>
  <NavBar/>
  
  
</template>
<script lang="ts">
import { defineComponent } from 'vue';
import NavBar from '../components/NavBar.vue'; // @ is an alias to /src
// Import other components if needed

export default defineComponent({
  name: 'HomePage',
  components: {
    NavBar,
    
  },
});
</script>

