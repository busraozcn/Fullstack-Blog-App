<template>
  <div>
    <!-- Yönetim arayüzü için HTML burada yer alacak -->
    <h1>Manage Data</h1>

    <!-- Butonlar -->
    <v-btn
      v-if="permissions.includes('manage-users')"
      @click="$router.push('/manage-users')"
      class="ma-2"
      color="primary"
    >
      Manage Users
    </v-btn>

    <v-btn
      v-if="permissions.includes('manage-todos')"
      @click="$router.push('/manage-todos')"
      class="ma-2"
      color="primary"
    >
      Manage Todos
    </v-btn>

    <v-btn
      v-if="permissions.includes('manage-posts')"
      @click="$router.push('/manage-posts')"
      class="ma-2"
      color="primary"
    >
      Manage Posts
    </v-btn>

    <v-btn
      v-if="permissions.includes('manage-albums')"
      @click="$router.push('/manage-albums')"
      class="ma-2"
      color="primary"
    >
      Manage Albums
    </v-btn>
  </div>
</template>

<script>
export default {
  name: "ManageData",
  data() {
    return {
      // Kullanıcının yetkileri, API'den veya başka bir kaynaktan dinamik olarak alınabilir
      permissions: [
        "manage-users",
        "manage-todos",
        "manage-posts",
        "manage-albums",
      ], // Tüm yetkilere sahip bir örnek kullanıcı
    };
  },
};
</script>

<style scoped>
/* Stil kuralları buraya gelecek */
</style>
