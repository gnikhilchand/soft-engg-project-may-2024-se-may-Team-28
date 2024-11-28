<template>
  <div>
    <NavBar/>
  

  <div class="courses-container">

    <div class="search-bar">

      <input v-model="searchQuery" @input="searchCourses" placeholder="Search courses...">

    </div>

    

    <div class="courses-grid">

      <div v-for="course in displayedCourses" :key="course.id" class="course-card" @click="openAssignmentsModal(course)">

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

    

    <div v-if="showModal" class="modal" @click="closeModal">

      <div class="modal-content" @click.stop>

        <span class="close" @click="closeModal">&times;</span>

        <h2>{{ selectedCourse.title }} - Assignments</h2>

        <table>

          <thead>

            <tr>

              <th>Title</th>

              <th>Description</th>

              <th>Due Date</th>

              <th>Actions</th>

            </tr>

          </thead>

          <tbody>

            <tr v-for="assignment in selectedCourse.assignments" :key="assignment.id">

              <td>{{ assignment.title }}</td>

              <td>{{ assignment.description }}</td>

              <td>{{ formatDate(assignment.due_date) }}</td>

              <td>

                <button @click="openUpdateAssignmentModal(assignment)" class="update-btn">Update</button>

                <button @click="deleteAssignment(assignment.id)" class="delete-btn">Delete</button>

              </td>

            </tr>

          </tbody>

        </table>

        <button @click="openCreateAssignmentModal" class="create-btn">Create New Assignment</button>

      </div>

    </div>



    <!-- Create/Update Assignment Modal -->

    <div v-if="showAssignmentModal" class="modal" @click="closeAssignmentModal">

      <div class="modal-content" @click.stop>

        <span class="close" @click="closeAssignmentModal">&times;</span>

        <h3>{{ isUpdating ? 'Update Assignment' : 'Create New Assignment' }}</h3>

        <form @submit.prevent="submitAssignment">

          <div>

            <label for="title">Title:</label>

            <input id="title" v-model="assignmentForm.title" required>

          </div>

          <div>

            <label for="description">Description:</label>

            <textarea id="description" v-model="assignmentForm.description"></textarea>

          </div>

          <div>

            <label for="due_date">Due Date:</label>

            <input id="due_date" v-model="assignmentForm.due_date" type="datetime-local">

          </div>

          <button type="submit">{{ isUpdating ? 'Update' : 'Create' }}</button>

        </form>

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

      showModal: false,

      selectedCourse: null,

      showAssignmentModal: false,

      isUpdating: false,

      assignmentForm: {

        id: null,

        title: '',

        description: '',

        due_date: '',

      },

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

    openAssignmentsModal(course) {

      this.selectedCourse = course;

      this.showModal = true;

    },

    closeModal() {

      this.showModal = false;

      this.selectedCourse = null;

    },

    formatDate(dateString) {

      if (!dateString) return 'Not specified';

      return new Date(dateString).toLocaleString();

    },

    openUpdateAssignmentModal(assignment) {

      this.isUpdating = true;

      this.assignmentForm = { ...assignment };

      this.showAssignmentModal = true;

    },

    openCreateAssignmentModal() {

      this.isUpdating = false;

      this.assignmentForm = {

        id: null,

        title: '',

        description: '',

        due_date: '',

      };

      this.showAssignmentModal = true;

    },

    closeAssignmentModal() {

      this.showAssignmentModal = false;

    },

    async submitAssignment() {

      try {

        if (this.isUpdating) {

          await this.updateAssignment();

        } else {

          await this.createAssignment();

        }

        this.closeAssignmentModal();

        await this.refreshCourseAssignments();

      } catch (error) {

        console.error('Error submitting assignment:', error);

      }

    },

    async createAssignment() {

      const response = await axios.post('http://127.0.0.1:8080/assignments', {

        ...this.assignmentForm,

        course_id: this.selectedCourse.id,

      });

      this.selectedCourse.assignments.push(response.data);

    },

    async updateAssignment() {

      const response = await axios.put(`http://127.0.0.1:8080/assignments/${this.assignmentForm.id}`, this.assignmentForm);

      const index = this.selectedCourse.assignments.findIndex(a => a.id === this.assignmentForm.id);

      if (index !== -1) {

        this.selectedCourse.assignments.splice(index, 1, response.data);

      }

    },

    async deleteAssignment(assignmentId) {

      if (confirm('Are you sure you want to delete this assignment?')) {

        try {

          await axios.delete(`http://127.0.0.1:8080/assignments/${assignmentId}`);

          this.selectedCourse.assignments = this.selectedCourse.assignments.filter(a => a.id !== assignmentId);

        } catch (error) {

          console.error('Error deleting assignment:', error);

        }

      }

    },

    async refreshCourseAssignments() {

      const response = await axios.get(`http://127.0.0.1:8080/courses/${this.selectedCourse.id}`);

      this.selectedCourse = response.data;

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