<!--PFP Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <div class="modal_title">User Profile</div>
      <input v-model="user_name" placeholder="Username" />
      <button @click="update_profile">Update Profile</button>
      <button @click="closeModal">X</button>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    props: ["show"],
    emits: ["close"], 
    components: { Modal }
}
</script>

<style scoped>
.modal_title {
  font-size: 3rem;
  color: #0E2F15;
  cursor: default;
}

.close_button {
  top: 95%;
  left: 95%;
  border-radius: 25px;
}
</style>