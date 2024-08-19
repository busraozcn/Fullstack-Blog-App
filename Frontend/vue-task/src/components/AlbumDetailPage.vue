<template>
  <div class="album-details-page">
    <div class="content">
      <div class="geritusu" @click="goBack">
        <img
          src="@/assets/tabler_square-rounded-arrow-left.png"
          alt="Go Home Icon"
          class="geritusu-icon"
        />
        <span class="geritusu-text">Go Albums</span>
      </div>
      <div class="photos-list">
        <div
          v-for="photo in photos"
          :key="photo.id"
          class="photo-card"
          @click="openPhoto(photo)"
        >
          <img :src="photo.thumbnailUrl" alt="Photo" />
        </div>
      </div>
      <ModalPhotoComponent
        :show="showModal"
        :photo="selectedPhoto"
        @close="closeModal"
      />
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import axios from "axios";
import ModalPhotoComponent from "./ModalPhotoComponent.vue";

export default {
  name: "AlbumDetailsPage",
  components: {
    ModalPhotoComponent,
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const photos = ref([]);
    const selectedUser = ref(null);
    const album = ref({});
    const showModal = ref(false);
    const selectedPhoto = ref({});

    const fetchAlbumAndPhotos = async (albumId) => {
      try {
        const albumResponse = await axios.get(
          `http://127.0.0.1:8000/api/albums/${albumId}/`
        );
        album.value = albumResponse.data;

        const photosResponse = await axios.get(
          `http://127.0.0.1:8000/api/photos/?album=${albumId}`
        );
        photos.value = photosResponse.data;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const openPhoto = (photo) => {
      selectedPhoto.value = photo;
      showModal.value = true;
    };

    const closeModal = () => {
      showModal.value = false;
      selectedPhoto.value = {};
    };

    const goBack = () => {
      const userId = route.query.userId;
      router.push(`/albums?userId=${userId}`);
    };

    onMounted(() => {
      const albumId = route.params.albumId;
      const userId = route.query.userId;
      if (albumId) {
        fetchAlbumAndPhotos(albumId);
      }
      if (userId) {
        fetchUser(userId);
      }
    });

    const fetchUser = async (userId) => {
      try {
        const userResponse = await axios.get(
          `https://jsonplaceholder.typicode.com/users/${userId}`
        );
        selectedUser.value = userResponse.data;
      } catch (error) {
        console.error("Error fetching user:", error);
      }
    };

    return {
      photos,
      selectedUser,
      album,
      showModal,
      selectedPhoto,
      goBack,
      openPhoto,
      closeModal,
    };
  },
};
</script>

<style>
.album-detail-page {
  display: flex;
}

.content {
  margin-left: 260px;
}

.photos-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 80px;
}

.photo-card {
  width: 200px;
  border-radius: 0px;
  overflow: hidden;
  cursor: pointer;
}
.photo-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.photo-card img {
  width: 100%;
  height: 150px;
  object-fit: cover;
}
</style>
