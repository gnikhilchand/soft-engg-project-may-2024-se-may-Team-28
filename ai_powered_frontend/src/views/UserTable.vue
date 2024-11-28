<template>
  <div>
    <NavBar/>
    <div class="user-table">
      <h2>User Table</h2>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Username</th>
            <th>Email</th>
            <th>Role</th>
            <th>Last Login</th>
            <th>User Created</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.username }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>{{ user.last_login }}</td>
            <td>{{ user.created_at }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['users']
  };
  </script>
  
  <style scoped>

.user-table {
  font-family: 'Roboto', sans-serif;
  margin-top: 20px;
}

.table-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
  text-align: center;
  text-transform: uppercase;
}

.table-container {
  overflow-x: auto;
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
  font-weight: 400;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #e0e0e0;
  transition: background-color 0.3s ease;
}

.table-row {
  transition: transform 0.3s ease;
}

.table-row:hover {
  transform: scale(1.02);
}
  </style>
  