<template>
  <v-container>
    <!-- Başlık ve Albüm Ekleme Butonu -->
    <v-row align="center" justify="space-between">
      <v-col cols="6">
        <h2>Albums</h2>
      </v-col>
      <v-col cols="6" class="text-right">
        <v-btn
          v-if="hasPermission('add_album')"
          color="primary"
          @click="openAddAlbumDialog"
          >+ Add Album</v-btn
        >
      </v-col>
    </v-row>

    <!-- Albüm Listesi -->
    <v-row>
      <v-col v-for="(album, index) in albums" :key="index" cols="12" md="6">
        <v-card outlined @click="goToPhotos(album.id)">
          <v-img
            :src="album.cover || 'https://via.placeholder.com/150'"
            height="200px"
            contain
          >
            <template v-slot:placeholder>
              <div
                class="d-flex align-center justify-center"
                style="height: 200px"
              >
                <v-progress-circular
                  indeterminate
                  color="primary"
                ></v-progress-circular>
              </div>
            </template>
          </v-img>
          <v-card-title>{{ album.title }}</v-card-title>
          <v-card-actions>
            <v-btn
              v-if="hasPermission('change_album')"
              icon
              @click.stop="openEditAlbumDialog(album)"
            >
              <v-icon>mdi-pencil</v-icon>
            </v-btn>
            <v-btn
              v-if="hasPermission('delete_album')"
              icon
              @click.stop="openDeleteAlbumDialog(album)"
            >
              <v-icon>mdi-delete</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Albüm Ekleme/Düzenleme Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline"
            >{{ editingAlbum ? "Edit" : "Add" }} Album</span
          >
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="albumForm.title"
              label="Album Title"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="saveAlbum">Save</v-btn>
          <v-btn color="grey" text @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Silme Onayı İçin Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Delete Album</v-card-title>
        <v-card-text> Are you sure you want to delete this album? </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="closeDeleteDialog">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deleteAlbum">Delete</v-btn>
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
      editingAlbum: false,
      valid: false,
      albumForm: {
        id: null,
        title: "",
      },
      albums: [],
      albumToDelete: null,
      selectedUserId: null,
      user_permissions: [], // Kullanıcının izinleri burada saklanacak
      rules: {
        required: (value) => !!value || "This field is required.",
      },
    };
  },
  computed: {
    filteredAlbums() {
      return this.albums;
    },
  },
  created() {
    this.loadUserPermissions(); // Kullanıcı izinlerini yükle
    this.selectedUserId = this.$route.query.userId;
    if (this.selectedUserId) {
      this.fetchAlbums();
    }
  },
  methods: {
    async fetchAlbums() {
      try {
        const response = await axios.get("/api/albums/", {
          params: { userId: this.selectedUserId },
        });

        const albums = response.data;

        const albumPromises = albums.map(async (album) => {
          const photosResponse = await axios.get(
            `/api/photos/?album=${album.id}`
          );
          album.photos = photosResponse.data.slice(0, 4);
          album.cover =
            album.photos.length > 0
              ? album.photos[0].url
              : "https://via.placeholder.com/150";
          return album;
        });

        this.albums = await Promise.all(albumPromises);
      } catch (error) {
        console.error("Error fetching albums:", error);
      }
    },
    goToPhotos(albumId) {
      const userId = this.$route.query.userId;
      this.$router.push(`/manage-photos?albumId=${albumId}&userId=${userId}`);
    },
    openAddAlbumDialog() {
      this.resetForm();
      this.dialog = true;
    },
    openEditAlbumDialog(album) {
      this.albumForm = { ...album };
      this.editingAlbum = true;
      this.dialog = true;
    },
    openDeleteAlbumDialog(album) {
      this.albumToDelete = album;
      this.deleteDialog = true;
    },
    resetForm() {
      this.albumForm = {
        id: null,
        title: "",
      };
      this.editingAlbum = false;
    },
    saveAlbum() {
      if (this.editingAlbum) {
        axios
          .put(`/api/albums/${this.albumForm.id}/`, this.albumForm)
          .then(() => {
            this.fetchAlbums();
            this.closeDialog();
          })
          .catch((error) => {
            console.error("Error updating album:", error);
          });
      } else {
        const newAlbum = {
          ...this.albumForm,
          userId: parseInt(this.selectedUserId),
        };
        axios
          .post("/api/albums/", newAlbum)
          .then(() => {
            this.fetchAlbums();
            this.closeDialog();
          })
          .catch((error) => {
            console.error("Error adding album:", error);
          });
      }
    },
    deleteAlbum() {
      if (this.albumToDelete) {
        axios
          .delete(`/api/albums/${this.albumToDelete.id}/`)
          .then(() => {
            this.fetchAlbums();
            this.closeDeleteDialog();
          })
          .catch((error) => {
            console.error("Error deleting album:", error);
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
