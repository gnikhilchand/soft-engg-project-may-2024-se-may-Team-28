<template>
    <div>
       <NavBar/>
      <div class="search-container">
        <label>Title:</label>
        <input type="text" v-model="titleQuery">
        <label>Author:</label>
        <input type="text" v-model="authorQuery">
        <label>Publisher:</label>
        <input type="text" v-model="publisherQuery">
        <label>Category:</label>
        <input type="text" v-model="categoryQuery">
        <button @click="searchBooks" class="button">Search</button>
      </div>
      <BookForm v-if="isFormOpen" :mode="formMode" :bookData="bookData" />
      <table class="book-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>ISBN</th>
            <th>Year</th>
            <th>Author</th>
            <th>Publisher</th>
            <th>Category</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="book in books" :key="book.id">
            <td>{{ book.id }}</td>
            <td>{{ book.title }}</td>
            <td>{{ book.isbn }}</td>
            <td>{{ book.year }}</td>
            <td>{{ book.author_name }}</td>
            <td>{{ book.publisher_name }}</td>
            <td>{{ book.category_name }}</td>
            <td>
            
            <button @click="openForm('edit', book)" class="button">Edit</button>
            <button @click="deleteBook(book.id)" class="button">Delete</button>
          </td>
          </tr>
        </tbody>
      </table>
      <div v-if="totalPages > 1" class="pagination">
        <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
        <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
      </div>
    </div>
  </template>
  
  <script>
  import BookForm from './BookForm.vue';
  import NavBar from '@/components/NavBar.vue';


export default {
  components: {
    NavBar,
    BookForm,

  },
    data() {
      return {
        books: [],
        totalPages: 0,
        currentPage: 1,
        titleQuery: '',
        authorQuery: '',
        publisherQuery: '',
        categoryQuery: '',
        isFormOpen: false,
      formMode: 'add', // 'add' or 'edit'
      bookData: {} 
      };
    },
    mounted() {
      this.fetchBooks();
    },
    methods: {
      fetchBooks() {
        const url = new URL('http://localhost:5000/api/books');
        url.searchParams.append('title', this.titleQuery);
        url.searchParams.append('author', this.authorQuery);
        url.searchParams.append('publisher', this.publisherQuery);
        url.searchParams.append('category', this.categoryQuery);
        url.searchParams.append('page', this.currentPage);
  
        fetch(url)
          .then(response => response.json())
          .then(data => {
            this.books = data.books;
            this.totalPages = data.pages;
            this.currentPage = data.current_page;
          })
          .catch(error => {
            console.error('Error fetching books:', error);
          });
      },
      searchBooks() {
        this.currentPage = 1;
        this.fetchBooks();
      },
      nextPage() {
        if (this.currentPage < this.totalPages) {
          this.currentPage++;
          this.fetchBooks();
        }
      },
      prevPage() {
        if (this.currentPage > 1) {
          this.currentPage--;
          this.fetchBooks();
        }
      },
      openForm(mode, book = {}) {
      this.isFormOpen = true;
      this.formMode = mode;
      this.bookData = mode === 'edit' ? { ...book } : {}; // Clone book data if editing
    },
    deleteBook(bookId) {
      if (confirm('Are you sure you want to delete this book?')) {
        fetch(`http://localhost:5000/api/books/${bookId}`, {
          method: 'DELETE'
        })
        .then(response => {
          if (response.ok) {
            alert('please refresh this page')
            this.fetchBooks();
          } else {
            console.error('Error deleting book:', response.statusText);
          }
        })
        .catch(error => {
          console.error('Error deleting book:', error);
        });
      }
    }
    }
  };
  </script>
  
  <style scoped>
.book-table {
  width: 100%;
  border-collapse: collapse;
}

.book-table th, .book-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: left;
}

.book-table th {
  background-color: #f2f2f2;
}

.book-table td {
  transition: background-color 0.3s;
}

.book-table tr:hover td {
  background-color: #f9f9f9;
}

.search-container {
  margin-bottom: 20px;
}

.search-container label {
  margin-right: 10px;
}

.search-container input[type="text"], .search-container button {
  padding: 8px;
  margin-right: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.search-container button {
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.search-container button:hover {
  background-color: #45a049;
}

.pagination {
  margin-top: 20px;
}

.pagination button {
  background-color: #008CBA;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.pagination button:hover {
  background-color: #005A79;
}

.pagination button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}
.button{
display: inline-block;
                    outline: none;
                    cursor: pointer;
                    font-size: 14px;
                    line-height: 1;
                    border-radius: 500px;
                    transition-property: background-color,border-color,color,box-shadow,filter;
                    transition-duration: .3s;
                    border: 1px solid transparent;
                    letter-spacing: 2px;
                    min-width: 160px;
                    text-transform: uppercase;
                    white-space: normal;
                    font-weight: 700;
                    text-align: center;
                    padding: 16px 14px 18px;
                    color: #fff;
                    background-color: #15883e;
                    height: 48px;
                    
                }
.button:hover{
                        background-color: #1db954;
                    }
                
</style>
