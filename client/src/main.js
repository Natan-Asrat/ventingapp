import { createApp } from 'vue';
import { createPinia } from 'pinia';
import Antd from 'ant-design-vue';

import App from './App.vue';
import router from './router';
import './assets/main.css';
import vClickOutside from "click-outside-vue3";

// Import our configured axios instance
import api from './api/axios';

import { createGtag } from "vue-gtag";
// Create app
const app = createApp(App);
const pinia = createPinia();
app.use(createGtag({
  config: { id: "G-3CTKDGJ34R" },
  pageTrackerScreenviewEnabled: true
}, router));
// Make axios available globally (optional)
app.config.globalProperties.$http = api;

// Use plugins
app.use(pinia);
app.use(router);
app.use(Antd);
app.directive("click-outside", vClickOutside);

// Mount the app
app.mount('#app');

// Export the axios instance for use in stores and components
export { api };
