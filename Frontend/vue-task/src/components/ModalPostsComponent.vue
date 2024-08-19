<template>
  <transition name="modal-posts">
    <div class="modal-mask" v-if="visible">
      <div class="modal-wrapper">
        <div class="modal-container">
          <div class="modal-header">
            <slot name="header">
              <h1>{{ post.title }}</h1>
            </slot>
            <button class="close" @click="close">
              <img
                src="@/assets/tabler_square-rounded-x.png"
                alt="Close Icon"
              />
            </button>
          </div>
          <div class="modal-body">
            <slot name="body">
              <div class="post-detail">
                <p>{{ post.body }}</p>
              </div>
              <div class="modal-separator"></div>
              <div class="comments-section">
                <h3>Comments:</h3>
                <ul>
                  <li
                    v-for="comment in comments"
                    :key="comment.id"
                    class="comment-item"
                  >
                    <div class="comment-avatar-name">
                      <img
                        :src="getGravatarUrl(comment.email)"
                        alt="User Avatar"
                        class="comment-avatar"
                      />
                      <div class="comment-name">
                        <h4>{{ comment.name }}</h4>
                      </div>
                    </div>
                    <div class="comment-body">
                      <p>{{ comment.body }}</p>
                    </div>
                  </li>
                </ul>
              </div>
            </slot>
          </div>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
import md5 from "md5";
import axios from "axios";

export default {
  name: "ModalPostsComponent",
  props: {
    visible: {
      type: Boolean,
      default: false,
    },
    post: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      comments: [],
    };
  },
  watch: {
    post(newPost) {
      if (newPost && newPost.id) {
        this.fetchComments(newPost.id);
      }
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
    getGravatarUrl(email) {
      const hash = md5(email.trim().toLowerCase());
      return `https://www.gravatar.com/avatar/${hash}?d=identicon`;
    },
    async fetchComments(postId) {
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/api/comments?postId=${postId}`
        );
        this.comments = response.data;
      } catch (error) {
        console.error("Error fetching comments:", error);
      }
    },
  },
};
</script>

<style>
.modal-mask {
  position: fixed;
  z-index: 9998;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-container {
  width: 70%;
  max-width: 1200px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.close {
  background: none;
  border: none;
  cursor: pointer;
}

.modal-body {
  display: flex;
  justify-content: space-between;
}

/* Scrollbar for webkit browsers */
.post-detail {
  overflow-y: scroll;
  scrollbar-color: #d8d9dd;
  scrollbar-width: thin;
  flex: 1;
  margin-right: 20px;
  color: #000000b2;
  max-height: 400px;
  overflow-y: auto;
  padding-right: 10px;
  border-right: 1px solid #d8d9dd;
}

/* Webkit scrollbar */
.post-detail::-webkit-scrollbar {
  width: 12px;
}

.post-detail::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 10px;
}

.post-detail::-webkit-scrollbar-thumb {
  background-color: #888;
  border-radius: 10px;
  border: 3px solid #f1f1f1;
}

.post-detail::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.comments-section {
  flex: 1;
  margin-right: 20px;
  color: #000000b2;
  max-height: 400px;
  overflow-y: scroll;
  padding-right: 10px;
  border-right: 1px solid #d8d9dd;
  scrollbar-color: #d8d9dd;
  scrollbar-width: thin;
}

.comments-section::-webkit-scrollbar {
  width: 12px; /* Scrollbar genişliği */
}

.comments-section::-webkit-scrollbar-track {
  background: #f1f1f1; /* Track rengi */
  border-radius: 10px; /* Track köşe yuvarlaklığı */
}

.comments-section::-webkit-scrollbar-thumb {
  background-color: #888; /* Scrollbar thumb rengi */
  border-radius: 10px; /* Thumb köşe yuvarlaklığı */
  border: 3px solid #f1f1f1; /* Thumb kenarlığı */
}

.comments-section::-webkit-scrollbar-thumb:hover {
  background: #555; /* Thumb hover rengi */
}
h3 {
  font-family: "Poppins";
  font-size: 20px;
  font-weight: 600;
  line-height: 32px;
  text-align: left;
  color: #26303e;
}
.comment-item {
  display: flex;
  align-items: flex-start;
  margin-bottom: 15px;
  flex-direction: column;
}
.comment-avatar-name {
  display: flex;
  align-items: center;
}

.comment-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
.comment-name {
  text-align: left;
}

.comment-body {
  margin-top: 5px;
  text-align: left;
  padding-left: 50px;
}

.comment-body p {
  margin: 5px 0 0;
  font-size: 14px;
}

.modal-separator {
  width: 1px;
  background-color: #d8d9dd;
  height: 100%;
}
</style>
