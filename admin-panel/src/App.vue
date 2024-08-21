<template>
  <v-app>
    <!-- Login sayfası dışındaki sayfalarda sidebar gösterilecek -->
    <v-layout v-if="$route.path !== '/login'">
      <v-navigation-drawer
        v-model="drawer"
        app
        expand-on-hover
        rail
        :mini-variant.sync="mini"
        mini-variant-width="80"
        width="256"
      >
        <v-list>
          <!-- Kullanıcı Bilgisi -->
          <v-list-item
            :prepend-avatar="
              user.avatar || 'https://randomuser.me/api/portraits/women/85.jpg'
            "
            :subtitle="user.email"
            :title="user.name"
          ></v-list-item>
        </v-list>

        <v-divider></v-divider>

        <!-- Menü Öğeleri -->
        <v-list dense nav>
          <!-- Ana Menü Öğeleri -->
          <v-list-item
            prepend-icon="mdi-home"
            title="Homepage"
            @click="$router.push('/home')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-account-plus"
            title="Add Admin"
            :disabled="!hasPermission('view_adminuser')"
            @click="$router.push('/add-admin')"
          ></v-list-item>

          <v-list-item
            prepend-icon="mdi-account-group"
            title="Manage Users"
            :disabled="!hasPermission('view_user')"
            @click="$router.push('/manage-users')"
          ></v-list-item>
        </v-list>

        <v-spacer></v-spacer>

        <!-- Logout Butonu -->
        <v-list dense nav>
          <v-list-item
            prepend-icon="mdi-logout"
            title="Logout"
            @click="logout"
          ></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main :class="{ 'content-shifted': !mini }">
        <router-view />
      </v-main>
    </v-layout>

    <!-- Login sayfasında sadece login formu gösterilecek -->
    <router-view v-else />
  </v-app>
</template>

<script>
import axios from "axios";

export default {
  name: "App",
  data() {
    return {
      drawer: true,
      mini: false,
      user: {
        name: "",
        email: "",
        avatar: "",
      },
      user_permissions: [],
    };
  },
  created() {
    this.setupAxios();
    this.loadUserDetails();
    this.loadUserPermissions();
    console.log(this.user_permissions); // İzinlerin doğru gelip gelmediğini kontrol etmek için
  },
  methods: {
    setupAxios() {
      const token = localStorage.getItem("access_token");
      if (token) {
        axios.defaults.headers.common["Authorization"] = `Bearer ${token}`;
      }
    },
    loadUserDetails() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const payload = JSON.parse(atob(token.split(".")[1]));
        this.user.name = payload.name || "Anonymous";
        this.user.email = payload.email || "unknown@example.com";
        this.user.avatar = payload.avatar || ""; // Eğer avatar bilgisi varsa kullan
      } else {
        this.$router.push("/login");
      }
    },
    loadUserPermissions() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const payload = JSON.parse(atob(token.split(".")[1]));
        this.user_permissions = payload.permissions || [];
        console.log(this.user_permissions);
      }
    },
    hasPermission(permission) {
      const result = this.user_permissions.some(
        (perm) => perm.codename === permission
      );
      console.log(`Checking permission: ${permission}, Result: ${result}`);
      return result;
    },
    hasPermission(permission) {
      const result = this.user_permissions.includes(permission);
      console.log(`Checking permission: ${permission}, Result: ${result}`);
      return result;
    },

    logout() {
      localStorage.removeItem("access_token");
      localStorage.removeItem("refresh_token");
      delete axios.defaults.headers.common["Authorization"];
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
.content-shifted {
  margin-left: 256px;
  transition: margin-left 0.3s ease;
}
</style>
