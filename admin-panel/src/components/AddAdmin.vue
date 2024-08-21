<template>
  <v-container>
    <v-card class="mx-auto" max-width="500">
      <v-toolbar color="transparent" flat>
        <v-toolbar-title>Add Admin</v-toolbar-title>
        <v-spacer></v-spacer>
      </v-toolbar>

      <v-container>
        <v-form v-model="form" @submit.prevent="onSubmit">
          <v-text-field
            v-model="firstName"
            :readonly="loading"
            :rules="[required]"
            label="First Name"
            clearable
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="lastName"
            :readonly="loading"
            :rules="[required]"
            label="Last Name"
            clearable
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="email"
            :readonly="loading"
            :rules="[required]"
            label="Email"
            clearable
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="username"
            :readonly="loading"
            :rules="[required]"
            label="Username"
            clearable
            class="mb-4"
          ></v-text-field>

          <v-text-field
            v-model="password"
            :readonly="loading"
            :rules="[required]"
            label="Password"
            type="password"
            clearable
            class="mb-4"
          ></v-text-field>

          <v-btn color="#737373" @click="openPermissionsModal">
            Permissions
          </v-btn>

          <!-- Permissions Modal -->
          <v-dialog v-model="permissionsModal" max-width="600px">
            <v-card>
              <v-card-title class="text-h5">Select Permissions</v-card-title>
              <v-card-text>
                <v-list dense>
                  <v-list-item
                    v-for="(item, index) in permissions"
                    :key="index"
                    @click="togglePermission(item)"
                  >
                    <v-list-item-action>
                      <v-checkbox
                        v-model="selectedPermissions"
                        :value="item.value"
                        :label="item.text"
                        color="primary"
                      ></v-checkbox>
                    </v-list-item-action>
                    <v-list-item-content>
                      <v-list-item-title v-text="item.text"></v-list-item-title>
                    </v-list-item-content>
                  </v-list-item>
                </v-list>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="primary" @click="closePermissionsModal">
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>

          <v-divider class="my-4"></v-divider>

          <v-btn
            :disabled="!form"
            :loading="loading"
            color="#5e17eb"
            variant="elevated"
            type="submit"
            block
          >
            Add Admin
          </v-btn>
        </v-form>
      </v-container>
    </v-card>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      form: false,
      firstName: null,
      lastName: null,
      email: null,
      username: null,
      password: null,
      loading: false,
      permissionsModal: false,
      permissions: [], // İzinler backend'den yüklenecek
      selectedPermissions: [],
    };
  },

  watch: {
    firstName() {
      this.validateForm();
    },
    lastName() {
      this.validateForm();
    },
    email() {
      this.validateForm();
    },
    username() {
      this.validateForm();
    },
    password() {
      this.validateForm();
    },
  },

  methods: {
    validateForm() {
      this.form =
        this.firstName &&
        this.lastName &&
        this.email &&
        this.username &&
        this.password;
    },

    required(v) {
      return !!v || "Field is required";
    },

    async onSubmit() {
      if (!this.form) return;

      this.loading = true;

      try {
        const adminData = {
          first_name: this.firstName,
          last_name: this.lastName,
          email: this.email,
          username: this.username,
          password: this.password,
          permissions: this.selectedPermissions,
        };

        // Token'ı local storage'dan al
        const token = localStorage.getItem("access_token");

        // Admin oluşturmak için doğru URL'yi kullanın ve Authorization header'ını ekleyin
        const response = await axios.post("/api/admin-users/", adminData, {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log("Admin created:", response.data);
        this.$router.push("/manage-users"); // Admin başarıyla eklendikten sonra yönlendirme yapabilirsiniz.
      } catch (error) {
        console.error("Error creating admin:", error);
      } finally {
        this.loading = false;
      }
    },

    openPermissionsModal() {
      this.fetchPermissions();
      this.permissionsModal = true;
    },

    closePermissionsModal() {
      this.permissionsModal = false;
    },

    togglePermission(permission) {
      const index = this.selectedPermissions.indexOf(permission.value);
      if (index > -1) {
        this.selectedPermissions.splice(index, 1);
      } else {
        this.selectedPermissions.push(permission.value);
      }
    },

    async fetchPermissions() {
      try {
        const response = await axios.get("/api/permissions/");
        this.permissions = response.data.map((perm) => ({
          text: perm.name,
          value: perm.codename,
        }));
      } catch (error) {
        console.error("Error fetching permissions:", error);
      }
    },
  },
};
</script>

<style scoped></style>
