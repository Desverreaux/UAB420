<!--Search Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
        <header class ="header">
            <div class = "modal_title">Search</div>
            <button class="close_button"@click="$emit('close')">X</button>
        </header>
      
        <div class="main">
          <input v-model="search_bar" placeholder="Search for plant" />
            <button class="search_button" @click="search_command">🔍</button>  
        </div>
    
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
.header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 1rem;

    padding: 0.5rem 1rem 0.25rem 1rem;
}

.modal_title {
  font-size: 3rem;
  color: #0E2F15;
  cursor: default;

  margin: 0;
  line-height: 1;
}

.close_button {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 2px solid #0E2F15;
  font-weight: bold;
  cursor: pointer;

  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
}

.main{
    display: flex;
    flex-direction: row;
    cursor: default;
}
</style>