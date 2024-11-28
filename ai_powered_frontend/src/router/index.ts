import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import HomePage from '../views/Home.vue';
import LoginForm from '../views/LoginForm.vue';
import UserSignup from '../views/UserSignup.vue';
import ExploreBook from '../views/ExploreBook.vue';
import BorrowRecord from '../views/BorrowRecord.vue';
import AdminDashboard from '../views/AdminDashboard.vue';
import AddBook from '../views/AddBook.vue';
import AddEntities from '../views/AddEntities.vue';
import NotFound from '../views/NotFound.vue';
import EditBooks from '../views/EditBooks.vue';
import EditEntities from '../views/EditEntities.vue'
import LibrarianDashboard from '../views/LibrarianDashboard.vue'
import UserDashboard from '../views/UserDashboard.vue'
import CodeEditor from '../views/CodeEditor.vue';
import Summarizer from '@/views/summarizer.vue';
import CourseList from '@/views/CourseList.vue';



const routes: Array<RouteRecordRaw> = [
  {
    path: '/home',
    name: 'home',
    component: HomePage,
    
  },
  {
    path: '/login',
    name: 'login',
    component: LoginForm,
  
  },
  {
    path: '/signup',
    name: 'signup',
    component: UserSignup,
    
  },
  {
    path: '/explore',
    name: 'explore',
    component: ExploreBook,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/course',
    name: 'course',
    component: CourseList,
    meta: {
      role: 'user'
    }
  },
  {
    path: '/editentities',
    name: 'editentities',
    component: EditEntities,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/useradmin',
    name: 'useradmin',
    component: LibrarianDashboard,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/editbooks',
    name: 'editbooks',
    component: EditBooks,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/borrowrecords',
    name: 'borrowrecords',
    component: BorrowRecord,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/borrow',
    name: 'borrow',
    component: BorrowRecord,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/admin',
    name: 'admin',
    component: AdminDashboard,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/addbook',
    name: 'addbook',
    component: AddBook,
    meta: {
      role: 'Admin'
    }
  },
  {
    path: '/addentities',
    name: 'addentities',
    component: AddEntities,
    meta: {
      role: 'Admin'
    }

  },
  {
    path: '/codeeditor',
    name: 'codeeditor',
    component: CodeEditor,
  

  },
  {
    path: '/summarizer',
    name: 'summarizer',
    component: Summarizer,
  

  },
  {
    path: '/user',
    name: 'user',
    component: UserDashboard,
    meta: {
      role: 'user'
    }

  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFound,
    meta: {
    }
  },

];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
});

router.beforeEach((to, from, next) => {
  const userData = localStorage.getItem('user');
  const user = userData ? JSON.parse(userData) : null;

  if (to.meta.role && (!user || user.role !== to.meta.role)) {
    return next({ name: 'Login' });  // Redirect to login if not logged in or if role doesn't match
  }
  next();
});


export default router;
