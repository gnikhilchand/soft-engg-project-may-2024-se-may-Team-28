<template>
  <div>
    <NavBar/>
    <div class="content-wrapper">
    <h2>Borrow Records</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Book Title</th>
            <th>Username</th>
            <th>Borrow Date</th>
            <th>Due Date</th>
            <th>Return Date</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in approvedRecords" :key="record.id">
            <td>{{ record.id }}</td>
            <td>{{ record.book_title }}</td>
            <td>{{ record.username }}</td>
            <td>{{ record.borrow_date }}</td>
            <td>{{ record.due_date }}</td>
            <td>{{ record.return_date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  
    <h2>Unapproved Borrow Records</h2>
    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Book Title</th>
            <th>Username</th>
            <th>Borrow Date</th>
            <th>Due Date</th>
            <th>Return Date</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="record in unapprovedRecords" :key="record.id">
            <td>{{ record.id }}</td>
            <td>{{ record.book_title }}</td>
            <td>{{ record.username }}</td>
            <td>{{ record.borrow_date }}</td>
            <td>{{ record.due_date }}</td>
            <td>{{ record.return_date }}</td>
            <td>
              <button @click="approveRecord(record.id)">Approve</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  </div>
</template>

  
  <script>
  import { defineComponent } from 'vue';
  import NavBar from '@/components/NavBar.vue';
  
export default defineComponent({
    components: {
      NavBar,

  },
    data() {
      return {
        approvedRecords: [],
        unapprovedRecords: []
      };
    },
    created() {
      this.fetchApprovedRecords();
      this.fetchUnapprovedRecords();
    },
    methods: {
      fetchApprovedRecords() {
        // Make API call to fetch approved borrow records
        fetch('http://localhost:5000/api/borrow-records')
          .then(response => response.json())
          .then(data => {
            this.approvedRecords = data.borrow_records;
          })
          .catch(error => {
            console.error('Error:', error);
          });
      },
      fetchUnapprovedRecords() {
        // Make API call to fetch unapproved borrow records
        fetch('http://localhost:5000/api/borrow-records/unapproved')
          .then(response => response.json())
          .then(data => {
            this.unapprovedRecords = data.unapproved_borrow_records;
          })
          .catch(error => {
            console.error('Error:', error);
          });
      },
      approveRecord(recordId) {
        // Make API call to approve borrow record
        fetch(`http://localhost:5000/api/approve-borrow-record/${recordId}`, {
          method: 'POST'
        })
        .then(response => response.json())
        .then(data => {
          console.log(data.message);
          // Refresh unapproved records after approval
          this.fetchUnapprovedRecords();
        })
        .catch(error => {
          console.error('Error:', error);
        });
      }
    }
  });
  </script>
  
  <style scoped>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f4f4f4;
  margin: 0;
  padding: 20px; /* Provides some spacing from the viewport edges */
  display: flex;
  justify-content: center;
  align-items: flex-start; /* Align items at the start to prevent vertical stretch */
  min-height: 100vh;
}

.content-wrapper {
  width: 100%;
  max-width: 1200px; /* Maximum width of the content */
  margin: auto; /* Centers the content wrapper */
  display: flex;
  flex-direction: column;
  align-items: center; /* Ensures that all children (including h2) are centered */
}

h2 {
  color: #333;
  margin-bottom: 20px;
  width: 100%; /* Ensures the heading spans the full width of the content-wrapper */
  text-align: center;
}

.table-container {
  overflow-x: auto; /* Allows for horizontal scrolling on smaller screens */
  margin-bottom: 40px;
  width: 90%; /* Adjusts the width of the container to not span the entire width of the content-wrapper */
  max-width: 1100px; /* Optional: limits the maximum width */
}

table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 10px; /* Adds border radius to the tables */
  overflow: hidden; /* Ensures the border radius clips the table content */
}

th, td {
  text-align: left;
  padding: 12px;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #4CAF50;
  color: white;
}

tr:nth-child(even) {
  background-color: #f2f2f2;
}

tr:hover {
  background-color: #ddd;
}
button {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-size: 16px;
  margin: 4px 2px;
  transition: background-color 0.3s ease;
  cursor: pointer;
  border-radius: 5px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
}

button:hover {
  background-color: #45a049;
}

button:focus {
  outline: none;
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px) scale(0.9);
  }
  50% {
    opacity: 0.5;
    transform: translateY(-10px) scale(0.95);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.content-wrapper {
  animation: fadeIn 1s ease-in-out;
}

  </style>
  