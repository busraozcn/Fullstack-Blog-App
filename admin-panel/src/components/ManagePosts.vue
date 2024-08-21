<template>
  <v-container>
    <v-row align="center" justify="space-between">
      <v-col cols="6">
        <h1>Manage Posts</h1>
      </v-col>
      <v-col cols="6" class="text-right">
        <v-btn
          v-if="hasPermission('add_post')"
          color="primary"
          @click="openAddPostDialog"
          >+ Add Post</v-btn
        >
      </v-col>
    </v-row>

    <!-- Post Listesi -->
    <v-row>
      <v-col>
        <v-card outlined>
          <v-data-table
            :headers="headers"
            :items="filteredPosts"
            item-value="id"
            class="elevation-1"
          >
            <template v-slot:item.actions="{ item }">
              <v-icon
                v-if="hasPermission('change_post')"
                @click="editPost(item)"
                >mdi-pencil</v-icon
              >
              <v-icon
                v-if="hasPermission('delete_post')"
                @click="openDeletePostDialog(item)"
                class="ml-3"
                >mdi-delete</v-icon
              >
            </template>
          </v-data-table>
        </v-card>
      </v-col>
    </v-row>

    <!-- Post Düzenlemek veya Eklemek İçin Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ editingPost ? "Edit" : "Add" }} Post</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-text-field
              v-model="postForm.title"
              label="Post Title"
              :rules="[rules.required]"
              required
            ></v-text-field>
            <v-text-field
              v-model="postForm.body"
              label="Post Body"
              :rules="[rules.required]"
              required
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="savePost">Save</v-btn>
          <v-btn color="grey" text @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Silme Onayı İçin Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Delete Post</v-card-title>
        <v-card-text>Are you sure you want to delete this post?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="closeDeleteDialog">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deletePost">Delete</v-btn>
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
      editingPost: false,
      valid: false,
      postForm: {
        id: null,
        title: "",
        body: "",
      },
      posts: [],
      postToDelete: null,
      user_permissions: [], // Kullanıcının izinleri burada saklanacak
      headers: [
        { text: "Title", value: "title" },
        { text: "Content", value: "body" },
        { text: "Actions", value: "actions", sortable: false },
      ],
      rules: {
        required: (value) => !!value || "This field is required.",
      },
    };
  },
  computed: {
    filteredPosts() {
      return this.posts;
    },
  },
  created() {
    this.loadUserPermissions(); // Kullanıcı izinlerini yükle
    const userId = this.$route.query.userId;
    if (userId) {
      this.fetchPosts(userId);
    }
  },
  methods: {
    async fetchPosts(userId) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/posts/?userId=${userId}`
        );
        this.posts = response.data;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    },
    openAddPostDialog() {
      this.resetForm();
      this.dialog = true;
    },
    resetForm() {
      this.postForm = {
        id: null,
        title: "",
        body: "",
      };
      this.editingPost = false;
    },
    async savePost() {
      const userId = this.$route.query.userId;
      try {
        if (this.editingPost) {
          await axios.put(
            `http://127.0.0.1:8000/api/posts/${this.postForm.id}/`,
            this.postForm
          );
        } else {
          const newPost = { ...this.postForm, userId: userId };
          await axios.post("http://127.0.0.1:8000/api/posts/", newPost);
        }
        this.fetchPosts(userId);
        this.closeDialog();
      } catch (error) {
        console.error("Error saving post:", error);
      }
    },
    editPost(item) {
      this.postForm = { ...item };
      this.editingPost = true;
      this.dialog = true;
    },
    async deletePost() {
      const userId = this.$route.query.userId;
      if (this.postToDelete) {
        try {
          await axios.delete(
            `http://127.0.0.1:8000/api/posts/${this.postToDelete.id}/`
          );
          this.fetchPosts(userId);
          this.closeDeleteDialog();
        } catch (error) {
          console.error("Error deleting post:", error);
        }
      }
    },
    openDeletePostDialog(item) {
      this.postToDelete = item;
      this.deleteDialog = true;
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
        console.log("Permissions from token:", this.user_permissions);
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
