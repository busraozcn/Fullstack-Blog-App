<template>
  <div class="todos-page">
    <div class="geritusu" @click="goBack">
      <img
        src="@/assets/tabler_square-rounded-arrow-left.png"
        alt="Go Home Icon"
        class="geritusu-icon"
      />
      <span class="geritusu-text">Go Home</span>
    </div>
    <div class="todos-container">
      <br />
      <br /><br />
      <ul>
        <li v-for="todo in todos" :key="todo.id" class="todo-item">
          <input type="checkbox" v-model="todo.completed" class="checkbox" />
          <span :class="{ completed: todo.completed }">{{ todo.title }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";

export default {
  name: "TodosPage",
  setup() {
    const router = useRouter();
    const route = useRoute();
    const todos = ref([]);
    const selectedUser = ref(null);

    const fetchUserAndTodos = async (userId) => {
      try {
        const userResponse = await axios.get(
          `http://127.0.0.1:8000/api/users/${userId}`
        );
        selectedUser.value = userResponse.data;

        const todosResponse = await axios.get(
          `http://127.0.0.1:8000/api/todos?user=${userId}`
        );
        todos.value = todosResponse.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const goBack = () => {
      router.push("/");
    };

    onMounted(() => {
      const userId = route.query.userId;
      if (userId) {
        fetchUserAndTodos(userId);
      }
    });

    return {
      todos,
      selectedUser,
      goBack,
    };
  },
};
</script>

<style>
.todos-page {
  display: flex;
}

.geritusu {
  display: flex;
  align-items: center;
  cursor: pointer;
  position: absolute;
  top: 10px;
  left: 280px; /* Sidebar genişliği kadar */
  margin-top: 50px;
}

.geritusu-icon {
  width: 24px;
  height: 24px;
  margin-right: 8px;
}

.geritusu-text {
  font-family: "Poppins", sans-serif;
  font-size: 20px;
  font-weight: 600;
  line-height: 20px;
  text-align: left;
}

.todos-container {
  margin-left: 300px; /* Sidebar genişliği ve biraz boşluk */
  padding: 20px;
}

ul {
  list-style-type: none; /* Başlangıç noktalarını kaldırmak için */
  padding: 0;
}

li.todo-item {
  text-align: left;
  height: 48px; /* Her bir todo maddesinin yüksekliği */
  display: flex;
  align-items: center;
  font-family: "Roboto", sans-serif; /* Yazı tipi Roboto */
  gap: 10px; /* Checkbox ile metin arasındaki boşluk */
  color: #485b69;
  font-size: 14px;
}

input[type="checkbox"] {
  appearance: none;
  width: 14px;
  height: 14px;
  border: 2px solid black;
  border-radius: 2px;
  position: relative;
  cursor: pointer;
  font-weight: 4000;
}

input[type="checkbox"]:checked {
  background-color: #4f359b;
  border: none;
}

input[type="checkbox"]:checked::after {
  content: "";
  position: absolute;
  top: 2px;
  left: 5px;
  width: 3px;
  height: 8px;
  border: solid white;
  border-width: 0 2px 2px 0;
  transform: rotate(45deg);
}
</style>
