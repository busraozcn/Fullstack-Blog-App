<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card class="pa-6" max-width="400">
      <v-card-title class="text-h5">Login</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="login">
          <v-text-field
            v-model="username"
            label="Username"
            required
          ></v-text-field>
          <v-text-field
            v-model="password"
            label="Password"
            type="password"
            required
          ></v-text-field>
          <v-btn block color="#5e17eb" type="submit">Login</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "LoginPage",
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("/api/login/", {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("access_token", response.data.access);
        localStorage.setItem("refresh_token", response.data.refresh);
        axios.defaults.headers.common[
          "Authorization"
        ] = `Bearer ${response.data.access}`;
        this.$router.push("/home");
      } catch (error) {
        alert("Login failed. Please check your credentials.");
        console.error("Login error:", error);
      }
    },
  },
};
</script>

<style scoped>
.v-card {
  background-color: #1e1e1e;
  color: white;
  width: 100%;
  max-width: 400px; /* Kartın genişliğini sınırla */
}
</style>
