<template>
  <div>
    <NavBar/>
  
    <div class="courses-container">
      <div class="search-bar">
        <input v-model="searchQuery" @input="searchCourses" placeholder="Search courses...">
      </div>

      <div class="courses-grid">
        <div v-for="course in displayedCourses" :key="course.id" class="course-card" @click="registerForCourse(course.id)">
          <div class="card-content">
            <h3>{{ course.title }}</h3>
            <p>{{ course.description }}</p>
          </div>
        </div>
      </div>

      <div class="pagination">
        <button @click="changePage(-1)" :disabled="currentPage === 1">Previous</button>
        <span>Page {{ currentPage }} of {{ totalPages }}</span>
        <button @click="changePage(1)" :disabled="currentPage === totalPages">Next</button>
      </div>

      <!-- Registration Modal -->
      <div v-if="showRegistrationModal" class="modal" @click="closeRegistrationModal">
        <div class="modal-content" @click.stop>
          <span class="close" @click="closeRegistrationModal">&times;</span>
          <h3>{{ registrationStatus }}</h3>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from '@/components/NavBar.vue';
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  components: {
    NavBar,
  },

  data() {
    return {
      courses: [],
      currentPage: 1,
      perPage: 10,
      totalCourses: 0,
      searchQuery: '',
      showRegistrationModal: false,
      registrationStatus: '',
    };
  },

  computed: {
    totalPages() {
      return Math.ceil(this.totalCourses / this.perPage);
    },

    displayedCourses() {
      return this.courses;
    },
  },

  methods: {
    async fetchCourses() {
      try {
        const response = await axios.get('http://127.0.0.1:8080/courses', {
          params: {
            page: this.currentPage,
            per_page: this.perPage,
            title: this.searchQuery,
          },
        });

        this.courses = response.data.courses;
        this.totalCourses = response.data.total;
      } catch (error) {
        console.error('Error fetching courses:', error);
      }
    },

    changePage(direction) {
      this.currentPage += direction;
      this.fetchCourses();
    },

    searchCourses() {
      this.currentPage = 1;
      this.fetchCourses();
    },
    getUserId() {
        const user = JSON.parse(localStorage.getItem("user"));
        if (user && user.id) {
            return user.id;
        } else {
            console.error('User not found in local storage or no user ID available');
            return null;
        }
    },

    async registerForCourse(courseId) {
      const userId = this.getUserId;
      if (!userId) {
        alert('User not logged in.');
        return;
      }

      try {
        await axios.post('http://127.0.0.1:8080/user/user/course/registration', {
          user_id: userId,
          course_id: courseId,
        });

        this.registrationStatus = 'Successfully registered for the course!';
      } catch (error) {
        this.registrationStatus = 'Error registering for the course.';
        console.error('Error registering for course:', error);
      } finally {
        this.showRegistrationModal = true;
      }
    },

    closeRegistrationModal() {
      this.showRegistrationModal = false;
    },
  },

  mounted() {
    this.fetchCourses();
  },
});
</script>

<style scoped>
.courses-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  perspective: 1000px;
}

.search-bar {
  margin-bottom: 20px;
}

.search-bar input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 25px;
  border: 2px solid #3498db;
  transition: all 0.3s ease;
}

.search-bar input:focus {
  outline: none;
  box-shadow: 0 0 10px rgba(52, 152, 219, 0.5);
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
}

.course-card {
  background-color: #f0f0f0;
  border-radius: 10px;
  padding: 15px;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 200px;
  overflow: hidden;
  transform-style: preserve-3d;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.course-card:hover {
  transform: translateY(-10px) rotateX(5deg);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
}

.card-content {
  transition: transform 0.3s ease;
}

.course-card:hover .card-content {
  transform: translateZ(20px);
}

.pagination {
  margin-top: 20px;
  text-align: center;
}

.pagination button {
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.pagination button:hover:not(:disabled) {
  background-color: #2980b9;
}

.pagination button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}

.modal {
  position: fixed;
  z-index: 1;
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
  border-radius: 10px;
  max-width: 80%;
  max-height: 80%;
  overflow-y: auto;
  box-shadow: 0 0 20px rgba(0, 0, 0, 0.2);
  animation: modalAppear 0.3s ease;
}

@keyframes modalAppear {
  from { opacity: 0; transform: scale(0.9); }
  to { opacity: 1; transform: scale(1); }
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
  cursor: pointer;
  transition: color 0.3s ease;
}

.close:hover,
.close:focus {
  color: #000;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f2f2f2;
}

.update-btn, .delete-btn, .create-btn {
  padding: 5px 10px;
  margin: 0 5px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.update-btn {
  background-color: #3498db;
  color: white;
}

.delete-btn {
  background-color: #e74c3c;
  color: white;
}

.create-btn {
  background-color: #2ecc71;
  color: white;
  margin-top: 20px;
}

.update-btn:hover, .delete-btn:hover, .create-btn:hover {
  filter: brightness(90%);
}
.modal-content form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.modal-content form div {
  display: flex;
  flex-direction: column;
}

.modal-content form label {
  margin-bottom: 5px;
}

.modal-content form input,
.modal-content form textarea {
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 3px;
}

.modal-content form button {
  align-self: flex-start;
  padding: 10px 20px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.modal-content form button:hover {
  background-color: #2980b9;
}
</style>