<template>
  <div>
    <NavBar/>
  <div class="container">
    <div class="tabs">
      <button class="tab" v-for="(tab, index) in tabs" :key="index" @click="activeTab = tab">{{ tab }}</button>
    </div>
    <div v-if="activeTab === 'Authors'" class="tab-content">
      <h2>Authors</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Biography</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="author in authors" :key="author.id">
            <td>{{ author.id }}</td>
            <td>{{ author.name }}</td>
            <td>{{ author.biography }}</td>
            <td>
              <button @click="openUpdateAuthorForm(author)">Update</button>
              <button @click="deleteAuthor(author.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="isUpdateFormOpen" class="update-form">
        <h3>Update Author</h3>
        <form @submit.prevent="submitUpdateAuthorForm">
          <label>Name:</label>
          <input type="text" v-model="updateAuthorForm.name" required>
          <label>Biography:</label>
          <textarea v-model="updateAuthorForm.biography" required></textarea>
          <button type="submit">Update</button>
          <button @click="closeUpdateAuthorForm">Cancel</button>
        </form>
      </div>
    </div>
    <div v-else-if="activeTab === 'Publishers'" class="tab-content">
      <h2>Publishers</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Address</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="publisher in publishers" :key="publisher.id">
            <td>{{ publisher.id }}</td>
            <td>{{ publisher.name }}</td>
            <td>{{ publisher.address }}</td>
            <td>
              <button @click="openUpdatePublisherForm(publisher)">Update</button>
              <button @click="deletePublisher(publisher.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="isUpdatePublisherFormOpen" class="update-form">
        <h3>Update Publisher</h3>
        <form @submit.prevent="submitUpdatePublisherForm">
          <label>Name:</label>
          <input type="text" v-model="updatePublisherForm.name" required>
          <label>Address:</label>
          <textarea v-model="updatePublisherForm.address" required></textarea>
          <button type="submit">Update</button>
          <button @click="closeUpdatePublisherForm">Cancel</button>
        </form>
      </div>
    </div>
    <div v-else class="tab-content">
      <h2>Categories</h2>
      <table class="data-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="category in categories" :key="category.id">
            <td>{{ category.id }}</td>
            <td>{{ category.name }}</td>
            <td>{{ category.description }}</td>
            <td>
              <button @click="openUpdateCategoryForm(category)">Update</button>
              <button @click="deleteCategory(category.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
      <div v-if="isUpdateFormOpen" class="update-form">
        <h3>Update Category</h3>
        <form @submit.prevent="submitUpdateCategoryForm">
          <label>Name:</label>
          <input type="text" v-model="updateCategoryForm.name" required>
          <label>Description</label>
          <textarea v-model="updateCategoryForm.description" required></textarea>
          <button type="submit">Update</button>
          <button @click="closeUpdateCategoryForm">Cancel</button>
        </form>
      </div>
    </div>
  </div>
</div>
</template>

<script>
  import { defineComponent } from 'vue';
import NavBar from '../components/NavBar.vue';
  
export default defineComponent({
    components: {
    NavBar,
  },
  data() {
    return {
      activeTab: 'Authors',
      tabs: ['Authors', 'Publishers', 'Categories'],
      authors: [],
      publishers: [],
      categories: [],
      isUpdateFormOpen: false,
      isUpdatePublisherFormOpen: false,
      updateAuthorForm: {
        id: null,
        name: '',
        biography: ''
      },
      updatePublisherForm: {
        id: null,
        name: '',
        address: ''
      },
      updateCategoryForm: {
        id: null,
        name: '',
        address: ''
      }
    };
  },
  mounted() {
    this.fetchAuthors();
    this.fetchPublishers();
    this.fetchCategories();
  },
  methods: {
    async fetchAuthors() {
      const response = await fetch('http://localhost:5000/api/authors');
      const data = await response.json();
      this.authors = data;
    },
    async fetchPublishers() {
      const response = await fetch('http://localhost:5000/api/publishers');
      const data = await response.json();
      this.publishers = data;
    },
    async fetchCategories() {
      const response = await fetch('http://localhost:5000/api/categories');
      const data = await response.json();
      this.categories = data;
    },
    openUpdateAuthorForm(author) {
      this.updateAuthorForm.id = author.id;
      this.updateAuthorForm.name = author.name;
      this.updateAuthorForm.biography = author.biography;
      this.isUpdateFormOpen = true;
    },
    closeUpdateAuthorForm() {
      this.isUpdateFormOpen = false;
    },
    async submitUpdateAuthorForm() {
      // Send update request to backend
      const response = await fetch(`http://localhost:5000/api/authors/${this.updateAuthorForm.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.updateAuthorForm.name,
          biography: this.updateAuthorForm.biography
        })
      });

      if (response.ok) {
        // Refresh authors data after successful update
        this.fetchAuthors();
        this.isUpdateFormOpen = false;
      } else {
        console.error('Failed to update author');
      }
    },
    async deleteAuthor(authorId) {
  const confirmDelete = confirm('Are you sure you want to delete this author?');
  if (!confirmDelete) return;

  try {
    const response = await fetch(`http://localhost:5000/api/authors/${authorId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      this.authors = this.authors.filter(author => author.id !== authorId);
      alert('Author deleted successfully! please refresh this page');
    } else {
      throw new Error('Failed to delete author');
    }
  } catch (error) {
    console.error(error);
    alert('Failed to delete author');
  }
},
openUpdatePublisherForm(publisher){
  this.updatePublisherForm.id = publisher.id;
      this.updatePublisherForm.name = publisher.name;
      this.updatePublisherForm.address = publisher.address;
      this.isUpdatePublisherFormOpen = true;
},
closeUpdatePublisherForm() {
      this.isUpdatePublisherFormOpen = false;
    },
    async submitUpdatePublisherForm() {
      const response = await fetch(`http://localhost:5000/api/publishers/${this.updatePublisherForm.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.updatePublisherForm.name,
          address: this.updatePublisherForm.address
        })
      });

      if (response.ok) {
        this.fetchPublishers();
        this.isUpdatePublisherFormOpen = false;
      } else {
        console.error('Failed to update Publisher');
      }
    },
    async deletePublisher(PublisherId) {
  const confirmDelete = confirm('Are you sure you want to delete this publisher?');
  if (!confirmDelete) return;

  try {
    const response = await fetch(`http://localhost:5000/api/publishers/${PublisherId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      // Remove the deleted author from the authors list
      this.authors = this.authors.filter(publisher => publisher.id !== PublisherId);
      alert('Publihser deleted successfully! please refresh this page');
    } else {
      throw new Error('Failed to delete publisher');
    }
  } catch (error) {
    console.error(error);
    alert('Failed to delete Publihser');
  }
},
openUpdateCategoryForm(category){
  this.updateCategoryForm.id = category.id;
      this.updateCategoryForm.name = category.name;
      this.updateCategoryForm.address = category.address;
      this.isUpdateFormOpen = true;
},
closeUpdateCategoryForm() {
      this.isUpdateCategoryFormOpen = false;
    },
    async submitUpdateCategoryForm() {
      const response = await fetch(`http://localhost:5000/api/categories/${this.updateCategoryForm.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          name: this.updateCategoryForm.name,
          description: this.updateCategoryForm.description
        })
      });

      if (response.ok) {
        this.fetchCategories();
        this.isUpdateFormOpen = false;
      } else {
        console.error('Failed to update categories');
      }
    },
    async deleteCategory(CategoryId) {
  const confirmDelete = confirm('Are you sure you want to delete this categories?');
  if (!confirmDelete) return;

  try {
    const response = await fetch(`http://localhost:5000/api/categories/${CategoryId}`, {
      method: 'DELETE'
    });

    if (response.ok) {
      
      this.authors = this.authors.filter(category => category.id !== CategoryId);
      alert('Category deleted successfully! please refresh this page');
    } else {
      throw new Error('Failed to delete category');
    }
  } catch (error) {
    console.error(error);
    alert('Failed to delete category');
  }
},

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
.data-table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}

.data-table th {
  background-color: #f2f2f2;
}
</style>
