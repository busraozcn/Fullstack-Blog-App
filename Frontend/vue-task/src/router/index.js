import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/components/HomePage.vue";
import TodosPage from "@/components/TodosPage.vue";
import PostsPage from "@/components/PostsPage.vue";
import AlbumsPage from "@/components/AlbumsPage.vue";
import AlbumDetailPage from "@/components/AlbumDetailPage.vue";

const routes = [
  {
    path: "/",
    component: HomePage,
  },
  {
    path: "/todos",
    component: TodosPage,
  },
  {
    path: "/posts",
    component: PostsPage,
  },
  {
    path: "/albums",
    component: AlbumsPage,
  },
  {
    path: "/albums/:albumId",
    component: AlbumDetailPage,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
