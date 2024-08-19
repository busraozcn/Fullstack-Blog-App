<template>
  <div class="albums-page">
    <div class="content">
      <div class="geritusu" @click="goBack">
        <img
          src="@/assets/tabler_square-rounded-arrow-left.png"
          alt="Go Home Icon"
          class="geritusu-icon"
        />
        <span class="geritusu-text">Go Home</span>
      </div>
      <div class="albums-list">
        <div
          v-for="album in albums"
          :key="album.id"
          class="album-card"
          @click="goToAlbum(album.id)"
        >
          <div class="album-thumbnails">
            <img
              v-for="(photo, index) in album.photos.slice(0, 4)"
              :key="index"
              :src="photo.thumbnailUrl"
              alt="Thumbnail"
            />
          </div>
          <div class="album-title">
            <h3>{{ album.title }}</h3>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from "vue";
import { useRouter, useRoute } from "vue-router";
import api from "@/api"; // axios'u içeren api.js dosyanızdan import edin

export default {
  name: "AlbumsPage",
  setup() {
    const router = useRouter();
    const route = useRoute();
    const albums = ref([]);
    const selectedUser = ref(null);

    const fetchUserAndAlbums = async (userId) => {
      try {
        const userResponse = await api.get(`/users/${userId}/`);
        selectedUser.value = userResponse.data;

        const albumsResponse = await api.get(`/albums/?user=${userId}`);
        const albumsData = albumsResponse.data;

        for (const album of albumsData) {
          const photosResponse = await api.get(`/photos/?album=${album.id}`);
          album.photos = photosResponse.data;
        }

        albums.value = albumsData;
      } catch (error) {
        console.error("Error fetching data:", error);
      }
    };

    const goBack = () => {
      router.push("/");
    };

    const goToAlbum = (albumId) => {
      const userId = route.query.userId;
      router.push(`/albums/${albumId}?userId=${userId}`);
    };

    onMounted(() => {
      const userId = route.query.userId;
      if (userId) {
        fetchUserAndAlbums(userId);
      }
    });

    return {
      albums,
      selectedUser,
      goBack,
      goToAlbum,
    };
  },
};
</script>

<style>
.albums-page {
  display: flex;
}

.content {
  margin-left: 260px;
  padding: 20px;
}

.albums-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-top: 80px;
}

.album-card {
  width: 318px;
  height: 256px;
  cursor: pointer;
  border: 1px solid #ccc;
  border-radius: 8px;
  overflow: hidden;
  text-align: center;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  padding-bottom: 10%;
  padding-left: 1%;
  padding-top: 1%;
  padding-right: 1%;
}

.album-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.album-thumbnails {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(2, 1fr);
  width: 100%;
  height: auto;
}

.album-thumbnails img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.album-title {
  padding: 10px;
  background: #fff;
}

.album-title h3 {
  margin: 0;
  font-size: 14px;
  font-weight: 400;
  color: #333;
}
</style>
