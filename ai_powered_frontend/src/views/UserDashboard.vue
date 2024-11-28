<template>
  <div>
    <NavBar/>
    <div class="container py-5">
      <div class="user-details mb-4">
        <h2>User Dashboard</h2>
        <div class="card">
          <div class="card-body">
            <h5 class="card-title">{{ userDetails.username }}</h5>
            <p class="card-text"><strong>Email:</strong> {{ userDetails.email }}</p>
            <p class="card-text"><strong>Role:</strong> {{ userDetails.role }}</p>
            <p class="card-text"><strong>Created At:</strong> {{ formatDate(userDetails.created_at) }}</p>
            <p class="card-text"><strong>Last Login:</strong> {{ formatDate(userDetails.last_login) }}</p>
          </div>
        </div>
      </div>
      
      <div class="courses">
        <h3>Enrolled Courses</h3>
        <div class="row">
          <div class="col-md-4" v-for="course in userDetails.courses" :key="course.id">
            <div class="card mb-4 box-shadow">
              <div class="card-body">
                <h5 class="card-title">{{ course.title }}</h5>
                <p class="card-text">{{ course.description }}</p>
                <div class="d-flex justify-content-between align-items-center">
                  <small class="text-muted">Created: {{ formatDate(course.created_at) }}</small>
                  <button @click="openAssignmentsModal(course)" class="btn btn-primary btn-sm">View Assignments</button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Assignments Modal -->
    <div v-if="showModal" class="modal" tabindex="-1" role="dialog" style="display: block;">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">{{ selectedCourse.title }} - Assignments</h5>
            <button type="button" class="close" @click="closeModal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <ul class="list-group">
              <li v-for="assignment in selectedCourse.assignments" :key="assignment.id" class="list-group-item d-flex justify-content-between align-items-center">
                {{ assignment.title }}
                <button @click="goToCodeEditor(assignment.id)" class="btn btn-success btn-sm">Submit</button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
    <div v-if="showModal" class="modal-backdrop fade show"></div>
  </div>
</template>

<script>
import { onMounted, ref } from 'vue';
import { defineComponent } from 'vue';
import { useRouter } from 'vue-router';
import NavBar from '../components/NavBar.vue';

export default defineComponent({
  components: {
    NavBar,
  },
  name: 'UserDashboard',
  setup() {
    const userDetails = ref({});
    const showModal = ref(false);
    const selectedCourse = ref({});
    const router = useRouter();

    const getUserIdFromLocalStorage = () => {
      const user = JSON.parse(localStorage.getItem('user'));
      return user && user.userid ? user.userid : null;
    };

    const fetchUserDetails = async (userId) => {
      try {
        const response = await fetch(`http://localhost:8080/user/dashboard/${userId}/details`, {
          method: 'GET',
        });
        if (!response.ok) throw new Error('Failed to fetch user details');
        const data = await response.json();
        userDetails.value = data;
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
    };

    const formatDate = (dateString) => {
      if (!dateString) return 'N/A';
      const options = { year: 'numeric', month: 'long', day: 'numeric' };
      return new Date(dateString).toLocaleDateString(undefined, options);
    };

    const openAssignmentsModal = (course) => {
      selectedCourse.value = course;
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
    };

    const goToCodeEditor = () => {
      router.push(`/codeeditor`);
    };

    onMounted(() => {
      const userId = getUserIdFromLocalStorage();
      if (userId) {
        fetchUserDetails(userId);
      } else {
        console.error('User ID not found in localStorage');
      }
    });

    return {
      userDetails,
      formatDate,
      showModal,
      selectedCourse,
      openAssignmentsModal,
      closeModal,
      goToCodeEditor,
    };
  },
});
</script>
  
  <style scoped>
  /* Styles for User Dashboard */

/* Container styles */
.container {
  max-width: 960px;
  margin: 0 auto;
}

/* User details section */
.user-details h2 {
  margin-bottom: 20px;
  color: #333;
}

.card {
  border: none;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 24px;
  margin-bottom: 10px;
}

.card-text {
  color: #666;
}

/* Issued books section */
.issued-books h3 {
  margin-top: 40px;
  margin-bottom: 20px;
  color: #333;
}

.card-img-top {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
  max-height: 200px;
  object-fit: cover;
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 20px;
  margin-bottom: 10px;
}

.card-text {
  color: #666;
}

.btn-outline-secondary {
  color: #333;
  border-color: #333;
}

.btn-outline-secondary:hover {
  background-color: #333;
  color: #fff;
}

/* Animation on hover */
.card:hover {
  transform: translateY(-5px);
  transition: all 0.3s ease;
}

.btn-outline-secondary:hover {
  transform: translateY(-2px);
  transition: all 0.3s ease;
}
.pdf-viewer-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.pdf-viewer-container {
  background-color: #fff;
  width: 90%;
  height: 90%;
  position: relative;
}

  </style>
  