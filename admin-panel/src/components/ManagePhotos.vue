<template>
  <v-container>
    <v-row align="center" justify="space-between">
      <v-col cols="6">
        <h1>Manage Photos</h1>
      </v-col>
      <v-col cols="6" class="text-right">
        <v-btn
          v-if="hasPermission('add_photo')"
          color="primary"
          @click="openAddPhotoDialog"
          >+ Add Photo</v-btn
        >
      </v-col>
    </v-row>

    <!-- Fotoğraf Listesi -->
    <v-row>
      <v-col v-for="(photo, index) in photos" :key="index" cols="12" md="3">
        <v-card outlined>
          <v-img :src="photo.url" height="200px" contain></v-img>
          <v-card-title>{{ photo.title }}</v-card-title>
          <v-card-actions>
            <v-btn
              v-if="hasPermission('change_photo')"
              icon
              @click="openEditPhotoDialog(photo)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              v-if="hasPermission('delete_photo')"
              icon
              @click="openDeletePhotoDialog(photo)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Fotoğraf Ekleme/Düzenleme Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline"
            >{{ editingPhoto ? "Edit" : "Add" }} Photo</span
          >
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="photoForm.title"
              label="Photo Title"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="photoForm.url"
              label="Photo URL"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="savePhoto">Save</v-btn>
          <v-btn color="grey" text @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Silme Onayı İçin Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Delete Photo</v-card-title>
        <v-card-text> Are you sure you want to delete this photo? </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="closeDeleteDialog">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deletePhoto">Delete</v-btn>
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
      editingPhoto: false,
      valid: false,
      photoForm: {
        id: null,
        title: "",
        url: "",
      },
      photos: [],
      photoToDelete: null,
      albumId: null,
      user_permissions: [], // Kullanıcının izinleri burada saklanacak
      rules: {
        required: (value) => !!value || "This field is required.",
      },
    };
  },
  created() {
    this.loadUserPermissions(); // Kullanıcı izinlerini yükle
    this.albumId = this.$route.query.albumId;
    if (this.albumId) {
      this.fetchPhotos();
    }
  },
  methods: {
    async fetchPhotos() {
      try {
        const response = await axios.get("/api/photos/", {
          params: { album: this.albumId },
        });
        this.photos = response.data;
      } catch (error) {
        console.error("Error fetching photos:", error);
      }
    },
    openAddPhotoDialog() {
      this.resetForm();
      this.dialog = true;
    },
    openEditPhotoDialog(photo) {
      this.photoForm = { ...photo };
      this.editingPhoto = true;
      this.dialog = true;
    },
    openDeletePhotoDialog(photo) {
      this.photoToDelete = photo;
      this.deleteDialog = true;
    },
    resetForm() {
      this.photoForm = {
        id: null,
        title: "",
        url: "",
      };
      this.editingPhoto = false;
    },
    savePhoto() {
      if (this.editingPhoto) {
        axios
          .put(`/api/photos/${this.photoForm.id}/`, this.photoForm)
          .then(() => {
            this.fetchPhotos();
            this.closeDialog();
          })
          .catch((error) => {
            console.error("Error updating photo:", error);
          });
      } else {
        const newPhoto = {
          ...this.photoForm,
          albumId: this.albumId,
        };
        axios
          .post("/api/photos/", newPhoto)
          .then(() => {
            this.fetchPhotos();
            this.closeDialog();
          })
          .catch((error) => {
            console.error("Error adding photo:", error);
          });
      }
    },
    deletePhoto() {
      if (this.photoToDelete) {
        axios
          .delete(`/api/photos/${this.photoToDelete.id}/`)
          .then(() => {
            this.fetchPhotos();
            this.closeDeleteDialog();
          })
          .catch((error) => {
            console.error("Error deleting photo:", error);
          });
      }
    },
    closeDialog() {
      this.dialog = false;
    },
    closeDeleteDialog() {
      this.deleteDialog = false;
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
  },
};
</script>

<style scoped>
.text-right {
  text-align: right;
}
</style>
