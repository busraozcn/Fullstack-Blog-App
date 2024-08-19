<template>
  <div class="sidebar">
    <div class="profile-card">
      <div class="profile-sidebar" v-if="user">
        <img
          :src="getGravatarUrl(user.email)"
          alt="Profile Picture"
          class="profile-img"
        />
        <div class="profile-info-sidebar">
          <h2>{{ user.name }}</h2>
          <p>{{ user.email }}</p>
        </div>
      </div>
    </div>
    <div class="separator"></div>
    <ul class="menu">
      <li class="menu-item" v-if="user">
        <router-link
          :to="{ path: '/todos', query: { userId: user.id } }"
          class="menu-link"
          :class="{ active: $route.path === '/todos' }"
        >
          <div class="active-rectangle" v-if="$route.path === '/todos'"></div>
          <img
            src="@/assets/tabler_checkup-list.png"
            alt="Todos Icon"
            class="menu-icon"
          />
          <span class="menu-text">Todos</span>
        </router-link>
      </li>
      <li class="menu-item" v-if="user">
        <router-link
          :to="{ path: '/posts', query: { userId: user.id } }"
          class="menu-link"
          :class="{ active: $route.path === '/posts' }"
        >
          <div class="active-rectangle" v-if="$route.path === '/posts'"></div>
          <img
            src="@/assets/tabler_notebook-1.png"
            alt="Posts Icon"
            class="menu-icon"
          />
          <span class="menu-text">Posts</span>
        </router-link>
      </li>
      <li class="menu-item" v-if="user">
        <router-link
          :to="{ path: '/albums', query: { userId: user.id } }"
          class="menu-link"
          :class="{ active: $route.path === '/albums' }"
        >
          <div class="active-rectangle" v-if="$route.path === '/albums'"></div>
          <img
            src="@/assets/tabler_photo-heart-1.png"
            alt="Albums Icon"
            class="menu-icon"
          />
          <span class="menu-text">Albums</span>
        </router-link>
      </li>
    </ul>
    <div class="footer">
      <img
        :src="require('@/assets/n2mobil.png')"
        alt="logo"
        class="footer-logo"
      />
      <span>N2Mobil</span>
    </div>
  </div>
</template>

<script>
import md5 from "md5";

export default {
  name: "SidebarComponent",
  props: {
    user: {
      type: Object,
      required: false,
    },
  },
  methods: {
    getGravatarUrl(email) {
      const hash = md5(email.trim().toLowerCase());
      return `https://www.gravatar.com/avatar/${hash}?d=identicon`;
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
  width: 260px;
  height: 100%;
  padding: 32px 0;
  gap: 0;
  border-right: 1px solid #d8d9dd;
}

.profile-card {
  width: 10px;
  flex-direction: row;
  text-align: left;
  margin-left: 0px;
}

.profile-sidebar {
  display: flex;
  align-items: center;
  text-align: left;
  padding: 0 1em;
  margin-bottom: 1em;
  flex-direction: row;
  text-align: left;
  margin-left: 0px;
}

.profile-img {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  margin-right: 2px;
}

.profile-info-sidebar h2 {
  font-family: Poppins;
  font-size: 14px;
  font-weight: bold;
  line-height: 27px;
  margin: 0;
  color: #26303e;
  margin-left: 3px;
}

.profile-info-sidebar p {
  font-family: Josefin Sans;
  font-size: 14px;
  font-weight: 300;
  line-height: 14px;
  text-decoration: underline;
  margin-left: 10px;
}

.separator {
  width: 100%;
  height: 1px;
  background-color: #d8d9dd;
  margin: 1em auto;
}

.menu {
  list-style: none;
  padding: 0;
  margin: 0;
  flex-grow: 1;
}

.menu-item {
  margin-bottom: 1em;
}

.menu-link {
  font-family: var(--font-family);
  font-size: var(--font-size);
  font-weight: var(--font-weight);
  line-height: 15px; /* Hover ve active class için aynı line-height */
  color: var(--text-color);
  text-decoration: none;
  display: flex;
  align-items: center;
  padding: 1em;
  border-radius: 0.25em;
  position: relative;
  transition: background-color 0.3s;
}

.menu-link:hover {
  background-color: var(--sidebar-item-hover);
  color: var(--text-color);
}

.menu-icon {
  margin-right: 10px;
  width: 24px;
  height: 24px;
  filter: invert(23%) sepia(50%) saturate(2092%) hue-rotate(235deg)
    brightness(89%) contrast(97%);
}

.menu-text {
  color: var(--text-color);
  opacity: 1;
}

.menu-link.active {
  background-color: var(--active-bg-color);
  color: var(--active-text-color);
}

.active-rectangle {
  position: absolute;
  left: -30px; /* Başlangıçta daha solda */
  top: 0;
  bottom: 0;
  width: 8px;
  background-color: var(--active-rect-color);
  border-top-left-radius: 0px;
  border-top-right-radius: 100px;
  border-bottom-left-radius: 0px;
  border-bottom-right-radius: 100px;
  transition: left 0.5s ease-in-out; /* Animasyon eklemek için */
}

.menu-link.active .active-rectangle {
  left: 0;
}

.footer {
  display: flex;
  align-items: right;
  justify-content: center;
  margin-top: auto;
  font-family: var(--font-family);
  font-size: var(--font-size);
  font-weight: bold;
  line-height: var(--line-height);
  color: var(--text-color);
  border-top: 1px solid #d8d9dd;
  padding: 10px 0;
}

.footer-logo {
  width: 20px;
  height: auto;
  margin-right: 0.5em;
}
</style>
