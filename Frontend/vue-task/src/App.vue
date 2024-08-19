<template>
  <div id="app">
    <SidebarComponent v-if="selectedUser && showSidebar" :user="selectedUser" />
    <div id="content">
      <router-view @user-selected="onUserSelected" />
    </div>
  </div>
</template>

<script>
import SidebarComponent from "@/components/sidebar/SidebarComponent.vue";
import api from "@/api";
import { ref, onMounted, watch } from "vue";
import { useRoute } from "vue-router";

export default {
  name: "App",
  components: {
    SidebarComponent,
  },
  setup() {
    const selectedUser = ref(null);
    const showSidebar = ref(false);
    const route = useRoute();

    const fetchUser = async (userId) => {
      try {
        const response = await api.get(`/users/${userId}/`);
        selectedUser.value = response.data;
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    };

    onMounted(() => {
      const userId = route.query.userId; // URL'den userId'yi alın
      if (userId) {
        fetchUser(userId);
        showSidebar.value = true;
      }
    });

    watch(route, (newRoute) => {
      const userId = newRoute.query.userId;
      if (userId) {
        fetchUser(userId);
        showSidebar.value = true;
      } else {
        showSidebar.value = false;
      }
    });

    const onUserSelected = (user) => {
      selectedUser.value = user;
      showSidebar.value = true;
    };

    return {
      selectedUser,
      showSidebar,
      onUserSelected,
    };
  },
};
</script>
<style>
@import url("https://fonts.googleapis.com/css2?family=Poppins:wght@400&display=swap");
@import url("https://fonts.googleapis.com/css2?family=Josefin+Sans:wght@400&display=swap");

#app {
  font-family: Avenir, Helvetica, Arial, Poppins, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  display: flex;
}

#content {
  margin-left: 0px; /* Sidebar genişliği kadar boşluk bırakın */
  padding: 20px;
  flex: 1;
}

#app > div {
  flex: 1;
}
</style>
