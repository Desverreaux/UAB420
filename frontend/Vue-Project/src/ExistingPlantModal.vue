<!--existing_plant Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <span classs="modal_title" modal_title>Existing Plant</span>
      <input v-model="search_bar" placeholder="Search for plant"/>
      <textarea class="plant_info">This should say some text about your plant </textarea>
      <button class="close_button" @click="closeModal">X</button>
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

.plant_info {
    resize: none;
}

.close_button {
  top: 95%;
  left: 95%;
  border-radius: 25px;
}
</style>