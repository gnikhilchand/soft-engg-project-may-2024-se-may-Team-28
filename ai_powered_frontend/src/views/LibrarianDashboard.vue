<template>
  <div>
    <NavBar/>
  
  <div class="dashboard">
    <h1 class="dashboard-title">Admin Dashboard</h1>
    <div class="filters">
      <input type="text" v-model="filter.username" placeholder="Username">
      <input type="text" v-model="filter.email" placeholder="Email">
      
      <button @click="applyFilters">Apply Filters</button>
    </div>
    <div class="user-table">
      <h2 class="table-title">User Table</h2>
      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Email</th>
              <th>Role</th>
              <th>Last Login</th>
              <th>User Created </th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in paginatedUsers" :key="user.id" class="table-row">
              <td>{{ user.id }}</td>
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.role }}</td>
              <td>{{ user.last_login }}</td>
              <td>{{ formatDateTime(user.created_at) }}</td>
              <td>
                <div class="action-dropdown">
                  <button class="action-btn">Actions</button>
                  <div class="dropdown-content">
                    <a href="#" @click="showUpdateForm(user)">Update</a>
                    <a href="#" @click="deleteUser(user)">Delete</a>
                  </div>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="pagination">
      <span class="pagination-text">Entries per page:</span>
      <select v-model="perPage" @change="updatePerPage" class="per-page-dropdown">
        <option value="5">5</option>
        <option value="10">10</option>
        <option value="20">20</option>
        <option value="50">50</option>
        <option value="100">100</option>
      </select>
      <button @click="prevPage" :disabled="currentPage === 1" class="pagination-btn prev-btn">Previous</button>
      <span class="pagination-info">Page {{ currentPage }} of {{ totalPages }}</span>
      <button @click="nextPage" :disabled="currentPage === totalPages" class="pagination-btn next-btn">Next</button>
    </div>

    <!-- Update Form -->
    <div v-if="isUpdateFormVisible" class="update-form">
      <h2>Update User</h2>
      <form @submit.prevent="submitUpdate">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" id="username" v-model="updateUserDetails.username" class="form-control">
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="updateUserDetails.email" class="form-control">
        </div>
        <!-- Add more fields as needed -->
        <button type="submit" class="btn btn-primary">Update</button>
        <button type="button" class="btn btn-secondary" @click="cancelUpdate">Cancel</button>
      </form>
    </div>
  </div>
  </div>
</template>
  
  <script>
import { format } from 'date-fns';
import { defineComponent } from 'vue';
import NavBar from '../components/NavBar.vue';
  
export default defineComponent({
    components: {
    NavBar,
  },


  data() {
    return {
      users: [],
      filter: {
        username: '',
        email: '',
        membership_type: ''
      },
      currentPage: 1,
      perPage: 10,
      totalPages: 1,
      updateUserDetails: null,
    isUpdateFormVisible: false
    };
  },
  computed: {
    filteredUsers() {
      let filteredUsers = this.users;
      if (this.filter.username) {
        filteredUsers = filteredUsers.filter(user => user.username.toLowerCase().includes(this.filter.username.toLowerCase()));
      }
      if (this.filter.email) {
        filteredUsers = filteredUsers.filter(user => user.email.toLowerCase().includes(this.filter.email.toLowerCase()));
      }
      if (this.filter.membership_type) {
        filteredUsers = filteredUsers.filter(user => user.membership_type === this.filter.membership_type);
      }
      return filteredUsers;
    },
    
    paginatedUsers() {
      const startIndex = (this.currentPage - 1) * this.perPage;
      return this.filteredUsers.slice(startIndex, startIndex + this.perPage);
    }
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await fetch(`http://localhost:8080/user/api/users?page=${this.currentPage}&per_page=${this.perPage}`);
        const data = await response.json();
        this.users = data.users;
        this.totalPages = data.total_pages;
      } catch (error) {
        console.error('Error fetching users:', error);
      }
    },
    applyFilters() {
      this.currentPage = 1;
      this.fetchUsers();
    },
    updatePerPage() {
      this.currentPage = 1;
      this.fetchUsers();
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
        this.fetchUsers();
      }
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
        this.fetchUsers();
      }
    },
    formatDateTime(dateTimeString) {
      const date = new Date(dateTimeString);
      return format(date, 'dd MMM yyyy'); // Format as '20 Aug 2023'
    },
    async updateUser(user) {
  try {
    const response = await fetch(`http://localhost:8080/user/api/users/${user.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        // Add any additional headers if needed, such as authentication token
      },
      body: JSON.stringify({
        username: user.username,
        email: user.email,
        role: user.role,
        membership_type: user.membership_type
        // Add any other fields you want to update
      })
    });
    if (response.ok) {
      // Handle success message or update UI accordingly
      console.log('User updated successfully');
      this.updateUserDetails = user; // Populate updateUserDetails
      this.isUpdateFormVisible = true; // Show the update form
    } else {
      // Handle error response
      console.error('Error updating user:', response.statusText);
    }
  } catch (error) {
    console.error('Error updating user:', error);
  }
},
showUpdateForm(user) {
      this.updateUserDetails = { ...user };
      this.isUpdateFormVisible = true;
    },
async submitUpdate() {
    try {
      const response = await fetch(`http://localhost:8080/user/api/users/${this.updateUserDetails.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          // Add any additional headers if needed, such as authentication token
        },
        body: JSON.stringify({
          username: this.updateUserDetails.username,
          email: this.updateUserDetails.email,
          role: this.updateUserDetails.role,
          membership_type: this.updateUserDetails.membership_type
          // Add any other fields you want to update
        })
      });
      if (response.ok) {
        // Handle success message or update UI accordingly
        console.log('User updated successfully');
        this.isUpdateFormVisible = false; // Hide the update form
        // Optionally, you can refresh the user list or fetch the updated user
        this.fetchUsers();
      } else {
        // Handle error response
        console.error('Error updating user:', response.statusText);
      }
    } catch (error) {
      console.error('Error updating user:', error);
    }
  },
  cancelUpdate() {
      this.isUpdateFormVisible = false;
  },

    async deleteUser(user) {
      try {
        const response = await fetch(`http://localhost:8080/user/api/users/${user.id}`, {
          method: 'DELETE',
          // Add any headers if needed
        });
        if (response.ok) {
          // Handle success message or update UI accordingly
          console.log('User deleted successfully');
          // You may want to remove the deleted user from the list
          this.users = this.users.filter(u => u.id !== user.id);
        } else {
          // Handle error response
          console.error('Error deleting user:', response.statusText);
        }
      } catch (error) {
        console.error('Error deleting user:', error);
      }
    }
  },
  mounted() {
    this.fetchUsers();
  },
});
</script>


  
  <style scoped>
  .dashboard {
    font-family: 'Roboto', sans-serif;
    padding: 20px;
    text-align: center;
  }
  
  .dashboard-title {
    font-size: 32px;
    margin-bottom: 20px;
    color: #333;
    text-transform: uppercase;
    letter-spacing: 1px;
  }
  
  .filters {
    margin-bottom: 20px;
  }
  
  .filters input {
    margin-right: 10px;
  }
  
  .filters button {
    padding: 8px 16px;
    background-color: #007bff; /* Blue color */
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .user-table {
    margin-top: 20px;
  }
  
  .table-title {
    font-size: 24px;
    margin-bottom: 20px;
    color: #4CAF50; /* Green color */
    text-align: center;
    text-transform: uppercase;
  }
  
  .table-container {
    overflow-x: auto;
    max-width: 90%; /* Shorter table width */
    margin: 0 auto;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    border-spacing: 0;
    background-color: #f8f8f8;
    border-radius: 8px;
    overflow: hidden;
  }
  
  th, td {
    padding: 15px;
    text-align: left;
  }
  
  th {
    background-color: #4CAF50; /* Green color */
    color: #fff; /* White text */
    font-weight: 600;
  }
  
  tr:nth-child(even) {
    background-color: #f2f2f2;
  }
  
  tr:hover {
    background-color: #e0e0e0;
    transition: background-color 0.3s ease;
  }
  
  .action-dropdown {
    position: relative;
  }
  
  .action-btn {
    background-color: #007bff; /* Blue color */
    color: #fff;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
  }
  
  .action-btn:hover {
    background-color: #0056b3; /* Darker blue on hover */
  }
  
  .dropdown-content {
    display: none;
    position: absolute;
    background-color: #fff;
    min-width: 120px;
    box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
    z-index: 1;
  }
  
  .dropdown-content a {
    color: #333;
    padding: 12px 16px;
    text-decoration: none;
    display: block;
  }
  
  .dropdown-content a:hover {
    background-color: #f2f2f2;
  }
  
  .action-dropdown:hover .dropdown-content {
    display: block;
  }
  
  .pagination {
    margin-top: 20px;
  }
  
  .pagination {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.pagination-text,
.pagination-info {
  margin-right: 10px;
}

.per-page-dropdown,
.pagination-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.per-page-dropdown {
  margin-right: 10px;
}

.pagination-btn {
  background-color: #007bff;
  color: #fff;
  transition: background-color 0.3s ease;
}

.pagination-btn:hover {
  background-color: #0056b3;
}

.prev-btn,
.next-btn {
  margin-right: 5px;
}

.prev-btn:disabled,
.next-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


.filters {
  margin-bottom: 20px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.filters input[type="text"],
.filters select {
  margin-right: 10px;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s ease;
}

.filters input[type="text"]:focus,
.filters select:focus {
  border-color: #007bff; /* Blue color */
  outline: none;
}

.apply-filters-btn {
  padding: 8px 16px;
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.apply-filters-btn:hover {
  background-color: #0056b3;
}
.update-form {
  margin-top: 20px;
  padding: 20px;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.update-form h2 {
  margin-bottom: 20px;
  font-size: 24px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  font-size: 18px;
  margin-bottom: 5px;
}

.form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-primary {
  background-color: #007bff;
  color: #fff;
}

.btn-secondary {
  background-color: #6c757d;
  color: #fff;
}

.btn-primary:hover,
.btn-secondary:hover {
  background-color: #0056b3;
}

  </style>
  
  
  