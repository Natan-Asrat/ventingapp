import { createRouter, createWebHistory } from 'vue-router';
import { useUserStore } from '@/stores/user';
import LandingPage from '@/views/LandingPage.vue';
import AuthPage from '@/views/auth/AuthPage.vue';
import Feed from '@/views/Feed.vue';
import NewPost from '@/views/NewPost.vue';
import ForgotPassword from '@/views/auth/ForgotPassword.vue';
import Profile from '@/views/Profile.vue';
const routes = [
  {
    path: '/',
    name: 'Home',
    component: LandingPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: { requiresAuth: true }
  },
  {
    path: '/login',
    name: 'Login',
    component: AuthPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/signup',
    name: 'Signup',
    component: AuthPage,
    meta: { requiresAuth: false }
  },
  {
    path: '/forgot-password',
    name: 'ForgotPassword',
    component: ForgotPassword,
    meta: { requiresAuth: false }
  },
  {
    path: '/home',
    name: 'Feed',
    component: Feed,
    meta: { requiresAuth: true }
  },
  {
    path: '/new-post',
    name: 'NewPost',
    component: NewPost,
    meta: { requiresAuth: true }
  },
  {
    path: '/success',
    name: 'Success',
    beforeEnter: () => {
      // Reload the page (forces full SPA reload)
      console.log("redirecting")
      window.location.reload();
      window.location.href = `/home?_v=${Date.now()}`;
    }  
  },

  // Add a catch-all route for 404s
  {
    path: '/:pathMatch(.*)*',
    redirect: '/'
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior() {
    // Always scroll to top when navigating to a new route
    return { top: 0 };
  },
});

// Navigation guard to check authentication
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore();
  
  // Check if the route requires authentication
  if (to.matched.some(record => record.meta.requiresAuth)) {
    // Check if user is authenticated
    const isAuthenticated = await userStore.checkAuth();
    
    if (!isAuthenticated) {
      // Redirect to login if not authenticated
      return next({ 
        name: 'Login',
        query: { redirect: to.fullPath } // Save the original path for redirect after login
      });
    }
  }
  
  next();
});

export default router;
