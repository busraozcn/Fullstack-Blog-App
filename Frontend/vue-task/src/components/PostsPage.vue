<template>
  <div class="posts-page">
    <div class="geritusu" @click="goBack">
      <img
        src="@/assets/tabler_square-rounded-arrow-left.png"
        alt="Go Home Icon"
        class="geritusu-icon"
      />
      <span class="geritusu-text">Go Home</span>
    </div>
    <div class="content">
      <br /><br /><br />
      <ul>
        <li v-for="post in posts" :key="post.id">
          <div>
            <h1>{{ post.title }}</h1>
          </div>
          <div>
            <p>{{ post.body }}</p>
          </div>
          <div class="seemoretusu" @click="openPost(post)">
            <span class="seemoretusu-text">See More </span>
            <img
              src="@/assets/tabler_square-rounded-arrow-right.png"
              alt="Go Home Icon"
              class="seemoretusu-icon"
            />
          </div>
          <div class="separator"></div>
        </li>
      </ul>
      <ModalPostsComponent
        :visible="showModal"
        :post="selectedPost"
        :comments="comments"
        @close="closeModal"
      />
    </div>
  </div>
</template>
<script>
import ModalPostsComponent from "./ModalPostsComponent.vue";
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";

export default {
  name: "PostsPage",
  components: {
    ModalPostsComponent,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const posts = ref([]);
    const showModal = ref(false);
    const selectedPost = ref({});
    const comments = ref([]);
    const selectedUser = ref(null);

    const fetchPosts = async (userId) => {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/posts/?userId=${userId}`
        );
        posts.value = response.data;
      } catch (error) {
        console.error("Error fetching posts:", error);
      }
    };

    const fetchUser = async (userId) => {
      try {
        const userResponse = await axios.get(
          `http://127.0.0.1:8000/api/users/${userId}`
        );
        selectedUser.value = userResponse.data;
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    };

    const fetchComments = async (postId) => {
      try {
        const commentsResponse = await axios.get(
          `http://127.0.0.1:8000/api/comments?postId=${postId}`
        );
        comments.value = commentsResponse.data;
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    };

    const openPost = (post) => {
      selectedPost.value = post;
      fetchComments(post.id);
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
      selectedPost.value = null;
      comments.value = [];
    };

    const goBack = () => {
      router.push("/");
    };

    onMounted(() => {
      const userId = route.query.userId;
      if (userId) {
        fetchPosts(userId);
        fetchUser(userId);
      }
    });

    return {
      posts,
      showModal,
      selectedPost,
      comments,
      selectedUser,
      goBack,
      openPost,
      closeModal,
    };
  },
};
</script>
<style>
.posts-page {
  display: flex;
}

.content {
  text-align: left;
  margin-left: 260px;
  padding: 20px;
  font-family: Poppins;
  font-size: 14px;
  font-weight: 400;
  line-height: 20px;
  letter-spacing: 0.02em;
  text-align: left;
  width: 1124px;
}
h1 {
  font-family: Poppins;
  font-size: 18px;
  height: 20px;
}
p {
  text-align: left;
  margin-left: 29px;
  color: #000000b2;
  margin-top: 10px;
}
.seemoretusu {
  font-family: Poppins;
  font-size: 14px;
  font-weight: 500;
  line-height: 20px;
  letter-spacing: 0.02em;
  text-align: right;
  text-decoration: none;
  padding: 1em;
  border-radius: 0.25em;
  transition: background-color 0.3s;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.seemoretusu-text {
  margin-right: 10px;
  font-size: 14px;
  position: relative;
}

.seemoretusu-icon {
  width: 32px;
  height: 32px;
  filter: invert(28%) sepia(63%) saturate(4598%) hue-rotate(236deg)
    brightness(84%) contrast(94%);
}
.separator {
  width: 100%;
  border-top: 1px solid #d8d9dd;
  margin: 10px 0;
}
</style>
