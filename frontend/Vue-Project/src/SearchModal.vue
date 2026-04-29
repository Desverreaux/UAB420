<!--Search Modal-->
<template>
    <Modal :show="show" @close="$emit('close')">
        <header class ="header">
            <div class = "modal_title">Search</div>
            <button class="close_button"@click="$emit('close')">X</button>
        </header>
      
        <div class="main">
            <div class="search_row">
                <input v-model="search_bar" placeholder="Search for plant" @keyup.enter="submit" />

                <button class="search_button" @click="submit">🔍</button>  
            </div>

            <p v-if="loading">Searching...</p>
            <p v-if="error_message" class="error_message">{{ error_message }}</p>

            <div class-results="results">
                <div v-for="plant in search_results" :key="plant.slug || plant.scientific_name" class="result_card">
                
                    <img v-if="plant.image_url" :src="plant.image_url" :alt="plant.common_name || plant.scientific_name" class="plant_image"/>

                    <div class="plant_info">
                        <strong>{{ plant.common_name || "Unknown Common Name" }}</strong>
                        <span>{{ plant.scientific_name || "Unknown Scientific Name" }}</span>
                        <span v-if="plant.family"> Family: {{ plant.family || "Unknown Plant Family" }}</span>
                    </div>
                </div>
            </div>
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
            search_bar: "",

            search_results: [],
            loading: false, 
            error_mesage: ""

        }
    },

    methods: {
        async submit() {
            if (!this.search_bar) return
            this.$emit("query", this.search_bar)

            this.loading = true
            this.error_message = ""
            this.search_results = []

            try {
                const response = await fetch(`/api/searchPlants?q${encodeURIComponent(this.search_bar)}`)

                if (!response.ok) {
                    throw new Error(`HTTP error --> Status: ${response.status}`)
                }

                const result = await response.json()

                this.search_results = result.data || []
            
            } catch (err) {
                console.error("Plant Search Failed: ", err)
                this.error_message = "Failed to search for plant."
            } finally {
                this.loading = false
            }
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
    flex-direction: column;
    gap: 1rem;
    cursor: default;
    color: #0E2F15;
}

.search_row {
    display: flex;
    flex-direction: row;
    gap: 0.5rem;
}

.search_button {
    cursor: pointer;
}

.results {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;

  max-height: 300px;
  overflow-y: auto;
}

.result_card {
  display: flex;
  gap: 0.75rem;
  align-items: center;

  padding: 0.75rem;
  border: 2px solid #0E2F15;
  border-radius: 12px;
  background-color: #FFFFFF;
}

.plant_image {
  width: 75px;
  height: 75px;
  object-fit: cover;
  border-radius: 8px;
}

.plant_info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}
</style>