<template>
  <v-container class="manage-todos">
    <!-- Add Todo Button -->
    <v-btn
      v-if="hasPermission('add_todo')"
      color="primary"
      @click="openAddTodoDialog"
      class="mb-4"
    >
      + Add Todo
    </v-btn>

    <!-- Todos'u Listelemek İçin v-data-table -->
    <v-data-table :headers="headers" :items="todos" class="elevation-1">
      <!-- Completed Checkbox -->
      <template v-slot:item.completed="{ item }">
        <v-checkbox
          v-model="item.completed"
          @change="updateTodo(item)"
        ></v-checkbox>
      </template>

      <!-- Title with Conditional Styling -->
      <template v-slot:item.title="{ item }">
        <span :class="{ completed: item.completed }">{{ item.title }}</span>
      </template>

      <!-- Actions (Edit and Delete) -->
      <template v-slot:item.actions="{ item }">
        <v-icon
          v-if="hasPermission('change_todo')"
          small
          class="mr-2"
          @click="editTodo(item)"
          >mdi-pencil</v-icon
        >
        <v-icon
          v-if="hasPermission('delete_todo')"
          small
          @click="openDeleteTodoDialog(item)"
          >mdi-delete</v-icon
        >
      </template>
    </v-data-table>

    <!-- Todo Düzenlemek veya Eklemek İçin Dialog -->
    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">{{ editingTodo ? "Edit" : "Add" }} Todo</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <!-- Todo metin girişi -->
            <v-text-field
              v-model="todoForm.title"
              label="Todo"
              :rules="[rules.required]"
              required
            ></v-text-field>

            <!-- Checkbox -->
            <v-checkbox
              v-model="todoForm.completed"
              label="Completed"
            ></v-checkbox>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="saveTodo">Save</v-btn>
          <v-btn color="grey" text @click="closeDialog">Cancel</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Silme Onayı İçin Dialog -->
    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Delete Todo</v-card-title>
        <v-card-text> Are you sure you want to delete this todo? </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" text @click="closeDeleteDialog">Cancel</v-btn>
          <v-btn color="red darken-1" text @click="deleteTodo">Delete</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  name: "TodosPage",
  data() {
    return {
      dialog: false,
      deleteDialog: false, // Silme dialog kontrolü için
      editingTodo: false,
      valid: false,
      todoForm: {
        id: null,
        title: "",
        completed: false,
      },
      todos: [], // Todos verisini burada tanımlıyoruz
      user_permissions: [], // Kullanıcı izinleri burada saklanacak
      headers: [
        { text: "Completed", value: "completed", align: "center" },
        { text: "Title", value: "title" },
        { text: "Actions", value: "actions", sortable: false, align: "center" },
      ],
      rules: {
        required: (value) => !!value || "This field is required.",
      },
      todoToDelete: null, // Silinecek todo'yu takip etmek için
    };
  },
  created() {
    this.loadUserPermissions(); // Kullanıcı izinlerini yükle
    const userId = this.$route.query.userId;
    if (userId) {
      this.fetchUserAndTodos(userId); // Kullanıcı Todos'unu getir
    }
  },
  methods: {
    async fetchUserAndTodos(userId) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/todos/?user=${userId}`
        );
        this.todos = response.data;
      } catch (error) {
        console.error("Error fetching todos:", error);
      }
    },
    async saveTodo() {
      const userId = this.$route.query.userId;
      try {
        if (this.editingTodo) {
          await axios.put(
            `http://127.0.0.1:8000/api/todos/${this.todoForm.id}/`,
            this.todoForm
          );
        } else {
          const newTodo = { ...this.todoForm, userId: userId };
          await axios.post("http://127.0.0.1:8000/api/todos/", newTodo);
        }
        this.fetchUserAndTodos(userId); // Listeyi güncelle
        this.closeDialog();
      } catch (error) {
        console.error("Error saving todo:", error);
      }
    },
    async updateTodo(item) {
      try {
        await axios.put(`http://127.0.0.1:8000/api/todos/${item.id}/`, item);
        this.fetchUserAndTodos(this.$route.query.userId); // Güncellenen listeyi yükle
      } catch (error) {
        console.error("Error updating todo:", error);
      }
    },
    async deleteTodo() {
      const userId = this.$route.query.userId;
      if (this.todoToDelete) {
        try {
          await axios.delete(
            `http://127.0.0.1:8000/api/todos/${this.todoToDelete.id}/`
          );
          this.fetchUserAndTodos(userId); // Listeyi güncelle
          this.closeDeleteDialog();
        } catch (error) {
          console.error("Error deleting todo:", error);
        }
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
    openAddTodoDialog() {
      this.resetForm();
      this.dialog = true;
    },
    resetForm() {
      this.todoForm = {
        id: null,
        title: "",
        completed: false,
      };
      this.editingTodo = false;
    },
    editTodo(item) {
      this.todoForm = { ...item };
      this.editingTodo = true;
      this.dialog = true;
    },
    openDeleteTodoDialog(item) {
      this.todoToDelete = item;
      this.deleteDialog = true;
    },
    closeDialog() {
      this.dialog = false;
    },
    closeDeleteDialog() {
      this.deleteDialog = false;
    },
  },
};
</script>

<style scoped>
.completed {
  text-decoration: line-through;
  color: grey;
}
</style>
