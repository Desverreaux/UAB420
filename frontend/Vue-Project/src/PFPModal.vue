<!--PFP Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">

      <header class="header">
        <div class="modal_title">User Profile</div>
        <button class="close_button" @click="$emit('close')">X</button>
      </header>
      
      <input v-model="user_name" placeholder="Username" />
      <button class="update_profile" @click="update_profile">Update Profile</button>
      
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
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #0E2F15;
  font-weight: bold;
  cursor: pointer;
}
</style>