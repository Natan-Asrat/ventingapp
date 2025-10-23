import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Antd from 'ant-design-vue';

import App from './App.vue';
import router from './router';
import './assets/main.css';

// Import our configured axios instance
import api from './api/axios';

// Create app
const app = createApp(App);
const pinia = createPinia();

// Make axios available globally (optional)
app.config.globalProperties.$http = api;

// Use plugins
app.use(pinia);
app.use(router);
app.use(Antd);

// Mount the app
app.mount('#app');

// Export the axios instance for use in stores and components
export { api };
