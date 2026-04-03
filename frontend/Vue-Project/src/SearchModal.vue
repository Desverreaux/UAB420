<!--Search Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
      <div class = "modal_title">Search</div>
      <input v-model="search_bar" placeholder="Search for plant" />
      <button class="search_button" @click="search_command">🔍</button>
      <button class ="close_button" @click="closeModal">X</button>
    </Modal>
</template>

<script>
import Modal from "./Modal.vue"

export default {
    props: ["show"],
    emits: ["close", "query"],
    components: { Modal },

    data() {
        return {
            search_bar: ""
        }
    },

    methods: {
        submit() {
            if (!this.search_bar) return
            this.$emit("query", this.search_bar)
            this.search_bar = ""
        }
    }
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