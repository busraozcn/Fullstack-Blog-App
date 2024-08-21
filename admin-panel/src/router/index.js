// router.js veya index.js

import { createRouter, createWebHistory } from "vue-router";
import HomePage from "../components/HomePage.vue";
import LoginPage from "../components/LoginPage.vue";
import AddAdmin from "../components/AddAdmin.vue";
import ManageUsers from "../components/ManageUsers.vue";
import ManageTodos from "@/components/ManageTodos.vue";
import ManagePosts from "@/components/ManagePosts.vue";
import ManageAlbums from "@/components/ManageAlbums.vue";
import ManageData from "@/components/ManageData.vue";
import ManagePhotos from "@/components/ManagePhotos.vue";

// Rotaları tanımlıyoruz
const routes = [
  { path: "/login", component: LoginPage },
  { path: "/home", component: HomePage },
  { path: "/add-admin", component: AddAdmin },
  { path: "/manage-users", component: ManageUsers },
  { path: "/manage-todos", component: ManageTodos },
  { path: "/manage-posts", component: ManagePosts },
  { path: "/manage-albums", component: ManageAlbums },
  { path: "/manage-data", component: ManageData },
  { path: "/manage-photos", component: ManagePhotos },
];

// Router oluşturuyoruz
const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Burada route guard ekliyoruz
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access_token"); // Token'ı kontrol ediyoruz
  if (!token && to.path !== "/login") {
    next("/login"); // Eğer token yoksa login sayfasına yönlendiriyoruz
  } else {
    next(); // Eğer token varsa ya da zaten login sayfasındaysa devam etmesine izin veriyoruz
  }
});

export default router;
