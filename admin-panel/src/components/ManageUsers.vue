<template>
  <v-container>
    <h1>Manage Users</h1>
    <v-btn
      v-if="hasPermission('add_user')"
      color="primary"
      @click="openAddUserDialog"
      >+ Add User</v-btn
    >

    <!-- Kullanıcıları Listelemek İçin v-data-table -->
    <v-data-table :headers="headers" :items="users" class="elevation-1">
      <template v-slot:item.actions="{ item }">
        <v-icon
          small
          class="mr-2"
          v-if="hasPermission('change_user')"
          @click="editUser(item)"
          >mdi-pencil</v-icon
        >
        <v-icon
          small
          v-if="hasPermission('delete_user')"
          @click="confirmDeleteUser(item)"
          >mdi-delete</v-icon
        >
      </template>
      <template v-slot:item.name="{ item }">
        <v-btn text @click="openManageModal(item)">{{ item.name }}</v-btn>
      </template>
    </v-data-table>

    <!-- Kullanıcı Ekleme/Düzenleme Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ editingUser ? "Edit" : "Add" }} User</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="userForm.name"
              label="Name"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="userForm.username"
              label="Username"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="userForm.email"
              label="Email"
              :rules="[rules.required, rules.email]"
              required
            ></v-text-field>
            <v-text-field
              v-model="userForm.phone"
              label="Phone"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="userForm.website"
              label="Website"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="userForm.company.name"
              label="Company Name"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="saveUser">Save</v-btn>
          <v-btn color="grey" text @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Silme Onay Dialogu -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Kullanıcıyı Sil</v-card-title>
        <v-card-text>
          Bu kullanıcıyı silmek istediğinize emin misiniz?
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="closeDeleteDialog">İptal</v-btn>
          <v-btn color="red darken-1" text @click="deleteUser">Evet, Sil</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Kullanıcı Yönetim Modalı -->
    <v-dialog v-model="manageDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">{{ selectedUser.name }}</v-card-title>
        <v-card-text>
          <v-btn block v-if="hasPermission('view_todo')" @click="goTo('todos')"
            >Manage Todos</v-btn
          >
          <v-btn block v-if="hasPermission('view_post')" @click="goTo('posts')"
            >Manage Posts</v-btn
          >
          <v-btn
            block
            v-if="hasPermission('view_album')"
            @click="goTo('albums')"
            >Manage Albums</v-btn
          >
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="closeManageDialog">Close</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      dialog: false,
      deleteDialog: false,
      manageDialog: false,
      valid: false,
      editingUser: false,
      userToDelete: null,
      selectedUser: {},
      userForm: {
        id: null,
        name: "",
        username: "",
        email: "",
        phone: "",
        website: "",
        company: {
          name: "",
        },
      },
      users: [],
      user_permissions: [], // Kullanıcının izinleri burada saklanacak
      headers: [
        { text: "Name", value: "name" },
        { text: "Username", value: "username" },
        { text: "Email", value: "email" },
        { text: "Phone", value: "phone" },
        { text: "Website", value: "website" },
        { text: "Company Name", value: "company.name" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      rules: {
        required: (value) => !!value || "This field is required.",
        email: (value) => {
          const pattern = /^[^@]+@[^@]+\.[^@]+$/;
          return pattern.test(value) || "Invalid email.";
        },
      },
    };
  },
  created() {
    this.fetchUsers();
    this.loadUserPermissions(); // Kullanıcı izinlerini yükle
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get("/api/users/");
        this.users = response.data;
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    },
    loadUserPermissions() {
      const token = localStorage.getItem("access_token");
      if (token) {
        const payload = JSON.parse(atob(token.split(".")[1]));
        this.user_permissions = payload.permissions || [];
        console.log("Permissions from token:", this.user_permissions); // İzinleri kontrol edin
      } else {
        console.error("No token found!");
      }
    },
    hasPermission(permission) {
      return this.user_permissions.includes(permission); // İzinleri kontrol eden fonksiyon
    },
    openAddUserDialog() {
      this.resetForm();
      this.dialog = true;
    },
    async saveUser() {
      if (this.$refs.form.validate()) {
        try {
          console.log(this.userForm); // Gönderilen veriyi kontrol et
          let response;
          if (this.editingUser) {
            response = await axios.put(
              `/api/users/${this.userForm.id}/`,
              this.userForm
            );
          } else {
            response = await axios.post("/api/users/bulk_create/", [
              {
                ...this.userForm,
                address: this.userForm.address || {
                  street: "",
                  suite: "",
                  city: "",
                  zipcode: "",
                  geo: {
                    lat: "",
                    lng: "",
                  },
                },
                company: this.userForm.company || {
                  name: "",
                  catchPhrase: "",
                  bs: "",
                },
              },
            ]);
          }
          this.fetchUsers();
          this.closeDialog();
        } catch (error) {
          console.error(
            "Error saving user:",
            error.response ? error.response.data : error.message
          );
        }
      }
    },
    editUser(user) {
      this.userForm = { ...user };
      this.editingUser = true;
      this.dialog = true;
    },
    confirmDeleteUser(user) {
      this.userToDelete = user;
      this.deleteDialog = true;
    },
    async deleteUser() {
      if (this.userToDelete) {
        try {
          await axios.delete(`/api/users/${this.userToDelete.id}/`);
          this.fetchUsers();
          this.closeDeleteDialog();
        } catch (error) {
          console.error("Error deleting user:", error);
        }
      }
    },
    closeDeleteDialog() {
      this.deleteDialog = false;
      this.userToDelete = null;
    },
    closeDialog() {
      this.dialog = false;
    },
    resetForm() {
      this.userForm = {
        id: null,
        name: "",
        username: "",
        email: "",
        phone: "",
        website: "",
        company: {
          name: "",
        },
      };
      this.editingUser = false;
    },
    openManageModal(user) {
      this.selectedUser = user;
      this.manageDialog = true;
    },
    closeManageDialog() {
      this.manageDialog = false;
    },
    goTo(option) {
      switch (option) {
        case "todos":
          this.$router.push({
            path: `/manage-todos`,
            query: { userId: this.selectedUser.id },
          });
          break;
        case "posts":
          this.$router.push({
            path: `/manage-posts`,
            query: { userId: this.selectedUser.id },
          });
          break;
        case "albums":
          this.$router.push({
            path: `/manage-albums`,
            query: { userId: this.selectedUser.id },
          });
          break;
      }
      this.closeManageDialog();
    },
  },
};
</script>

<style scoped>
.v-btn {
  margin: 10px 0;
}
</style>
