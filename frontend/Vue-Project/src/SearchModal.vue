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
    emits: ["close", "add"],
    components: { Modal },

    data() {
        return {
            plantName: ""
        }
    },

    methods: {
        submit() {
            if (!this.plantName) return
            this.$emit("add", this.plantName)
            this.plantName = ""
        }
    }
}
</script>