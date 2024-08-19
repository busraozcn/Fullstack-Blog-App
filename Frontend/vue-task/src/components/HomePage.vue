<template>
  <div class="homepage">
    <div class="sidebar">
      <ul class="menu">
        <li class="menu-item">
          <router-link
            to="/"
            class="menu-link"
            :class="{ active: $route.path === '/' }"
          >
            <img
              src="@/assets/tabler_users.png"
              alt="Users Icon"
              class="users-icon"
            />
            <span class="menu-text">Users</span>
          </router-link>
        </li>
      </ul>
      <div class="footer">
        <img
          :src="require('@/assets/n2mobil.png')"
          alt="n2mobillogo"
          class="footer-logo"
        />
        <div class="footer-name">
          <h4>N2Mobil</h4>
        </div>
      </div>
    </div>
    <div class="main-content">
      <h1>All users</h1>
      <div class="user-container">
        <div
          v-for="user in users"
          :key="user.id"
          class="profile"
          :class="{ selected: user.id === selectedUserId }"
          @click="selectUser(user)"
        >
          <div class="profile-header">
            <img
              :src="getGravatarUrl(user.email)"
              alt="Profile Picture"
              class="profile-img"
            />
            <div class="user-info">
              <h2>{{ user.name }}</h2>
              <p>{{ user.email }}</p>
              <p>{{ user.phone }}</p>
            </div>
          </div>
          <div class="infos">
            <div class="location-info">
              <img
                src="@/assets/tabler_map-pin-heart.png"
                alt="Location Icon"
              />
              <div>
                <h3>Location</h3>
                <p>{{ user.address.city }}, {{ user.address.street }}</p>
              </div>
            </div>
            <div class="company-info">
              <img
                src="@/assets/tabler_building-skyscraper.png"
                alt="Company Icon"
              />
              <div>
                <h3>Company</h3>
                <p>{{ user.company.name }}</p>
              </div>
            </div>
            <div class="website-info">
              <img src="@/assets/tabler_world-share.png" alt="Website Icon" />
              <div>
                <h3>Website</h3>
                <p>{{ user.website }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from "@/api";
import md5 from "md5";

export default {
  name: "HomePage",
  data() {
    return {
      users: [],
      selectedUserId: null,
    };
  },
  created() {
    this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await api.get("/users/");
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    getGravatarUrl(email) {
      const cleanedEmail = email.trim().toLowerCase();
      const hash = md5(cleanedEmail);
      return `https://www.gravatar.com/avatar/${hash}?d=identicon`;
    },
    selectUser(user) {
      this.selectedUserId = user.id;
      this.$router.push({ path: "/todos", query: { userId: user.id } });
    },
  },
};
</script>

<style>
:root {
  --sidebar-bg-color: #f5f5f5;
  --sidebar-item-hover: #ffffff;
  --font-family: "Poppins", sans-serif;
  --font-size: 18px;
  --font-weight: 400;
  --line-height: 27px;
  --text-color: #00000073;
  --active-bg-color: #ffffff;
  --active-rect-color: #4f359b;
  --active-text-color: #4f359b;
}

.homepage {
  display: flex;
}

.sidebar {
  color: var(--text-color);
  background-color: var(--sidebar-bg-color);
  position: fixed;
  z-index: 1;
  top: 0;
  left: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  width: 240px;
  padding: 32px 0px 32px 0px;
  gap: 0px;
  border-right: 1px solid #d8d9dd;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
}

.menu-item {
  margin-left: 5px;
  margin-bottom: 0.5em;
}

.menu-link {
  font-family: var(--font-family);
  font-size: var(--font-size);
  font-weight: var(--font-weight);
  line-height: var(--line-height);
  color: var(--text-color);
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 0.5em 1em;
  border-radius: 0.25em;
  transition: background-color 0.3s;
  position: relative;
  width: 220px;
  height: 27px;
  gap: 12px;
}

.menu-link::before {
  content: "";
  position: absolute;
  left: 0;
  top: 0;
  bottom: 0;
  width: 4px;
  background-color: transparent;
  transition: background-color 0.3s;
  border-radius: 10px; /* Border-radius value increased */
}

.menu-link.active {
  background-color: var(--active-bg-color);
  color: var(--active-text-color);
}

.menu-link.active::before {
  background-color: var(--active-rect-color);
  width: 6px;
}

.menu-link:hover {
  background-color: var(--sidebar-item-hover);
  color: black;
}

.menu-text {
  color: var(--text-color);
  opacity: 1;
}

.menu-link.active .menu-text {
  color: var(--active-text-color);
}

.footer {
  display: flex;
  align-items: center;
  width: 228px;
  height: 40px;
  gap: 8px;
  opacity: 1;
  border-top: 1px solid #d8d9dd;
  margin-top: auto;
  padding: 10px 0;
  font-family: var(--font-family);
  font-size: var(--font-size);
  font-weight: bold;
  line-height: var(--line-height);
  color: var(--text-color);
  margin-bottom: 40px;
  margin-left: 7px;
}

.footer-name {
  font-family: "Poppins", sans-serif;
  font-size: 22px;
  font-weight: 700;
  line-height: 33px;
  text-align: left;
  color: #485b69;
}
h4 {
  font-family: Poppins;
  font-size: 18px;
  line-height: 1.5;
}
.footer-logo {
  width: 50px;
  height: auto;
  margin-right: 0.5em;
}

.main-content {
  padding-left: 220px;
  padding-top: 20px;
}

.user-container {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-left: 0px;
}

.profile {
  background-color: #ffffff;
  padding: 20px 24px;
  border-radius: 12px;
  border: 1px solid #d8d9dd;
  cursor: pointer;
  transition: box-shadow 0.3s;
  width: 320px;
  height: 380px;
  margin-left: 28px;
  gap: 20px;
}
.profile.selected {
  border-color: #4f359b;
  background-color: #e7f1ff;
}
.profile:hover {
  box-shadow: 12px 12px 12px rgba(0.1, 0.1, 0.1, 0.1);
}
.profile-header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.profile-img {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-bottom: 10px;
}

.user-info {
  text-align: left;
  margin-left: 20px;
}
.profile-img {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  margin-right: 20px;
}
h1 {
  text-align: left;
  margin-left: 30px;
  margin-top: 0px;
}

h2 {
  font-size: 18px;
  font-family: Poppins;
  font-weight: 500;
  line-height: 1.2;
}

h3 {
  font-family: Poppins;
  font-size: 14px;
  font-weight: 500;
  line-height: 1.5;
  margin-bottom: 5px;
}

p {
  font-family: Poppins;
  font-size: 13px;
  line-height: 1.5;
  margin: 0;
}

.infos {
  display: flex;
  flex-direction: column;
  text-align: left;
}

.infos > div {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
  text-align: left;
}

.infos > div > img {
  margin-right: 10px;
  width: 24px;
  height: 24px;
}
</style>
