<template>
  <div class="modal" v-if="show" @click.self="close">
    <div class="modal-content">
      <span class="close" @click="close">&times;</span>
      <img :src="photo.url" alt="Photo" class="modal-photo" />
      <p>{{ photo.title }}</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "ModalPhotoComponent",
  props: {
    show: {
      type: Boolean,
      required: true,
    },
    photo: {
      type: Object,
      required: true,
    },
  },
  methods: {
    close() {
      this.$emit("close");
    },
  },
};
</script>

<style>
.modal {
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
.modal-content {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
  text-align: center;
  position: relative;
}
.close {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  position: absolute;
  top: 10px;
  right: 10px;
}
.modal-photo {
  width: 100%;
  height: auto;
  max-width: 500px;
  max-height: 500px;
}
</style>
