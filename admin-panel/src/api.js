// src/main.js

import { createApp } from "vue";
import App from "./App.vue";
import axios from "axios";

// Axios baseURL yapılandırması
axios.defaults.baseURL = "http://localhost:8000";

const app = createApp(App);

// Axios'u global olarak erişilebilir hale getirme
app.config.globalProperties.$axios = axios;

app.mount("#app");
