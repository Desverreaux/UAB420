<template> <!-- HTML -->
	<div class="page">
    <header class="header">
      <div 
        class="title">Thirsty Plant
      </div>

      <div class="UIElements">
        <button 
          class="Guide"
          @click="openModal('Guide')">Guide
        </button>

        <button
          class="Search"
          @click="openModal('Search')">Search
        </button>

        <div>
          <a href="http://uab420.desverreaux.com:8978" target="_blank" rel="noopener">Database</a>
        </div> 

        <button
          class="PFP"
          @click="openModal('PFP')">👤
        </button>

      </div>
    </header>
		
    <main class="main">
      <div class="plant_card" @click="openModal('existing_plant')">
        <div class="status_icon" :class="plant_status">
          <span v-if="plant_status === 'good'">✓</span>
          <span v-else-if="plant_status === 'warning'">⚠️</span>
          <span v-else>❗</span>
        </div>

        <div class="plant_icon">🪴</div>

        <div class="moisture_percentage">
          {{ moisture_percentage }}
        </div>
      </div>

      <!--
      <button 
        class="existing_plant"
        @click="openModal('existing_plant')">🪴
      </button>
      -->

      <button 
        class="new_plant"
        @click="openModal('new_plant')">+
      </button>

      <!-- Chart.js test - remove once verified -->
      <div style="background:#fff; border-radius:12px; padding:1rem; width:300px; height:220px;">
        <canvas ref="testChart"></canvas>
      </div>

    </main>

    <!--Guide Modal-->
    <GuideModal 
      :show="activeModal === 'Guide'" 
      @close="closeModal"
    />

    <!--Search Modal-->
    <SearchModal 
      :show="activeModal === 'Search'" 
      @close="closeModal"
    />

    <!--PFP Modal-->
    <PFPModal 
      :show="activeModal === 'PFP'" 
      @close="closeModal"
    />
    
    <!--existing_plant Modal-->
    <ExistingPlantModal 
      :show="activeModal === 'existing_plant'" 
      @close="closeModal"
    />

    <!--new_plant Modal [IM NOT SURE YET IF THIS WILL BE NEEDED SINCE THIS ROUTES TO THE SEARCH FEATURE]-->

    <CriticalErrorModal 
      :show="activeModal === 'critical_error'" 
      :error="errorMessage"
      @close="closeModal"
    />
	</div>
</template>

<script>
import { Chart as ChartJS, BarController, BarElement, CategoryScale, LinearScale } from "chart.js"
import { Chart } from "vue-chartjs"
import GuideModal from "./GuideModal.vue"
import SearchModal from "./SearchModal.vue"
import PFPModal from "./PFPModal.vue"
import ExistingPlantModal from "./ExistingPlantModal.vue"
import CriticalErrorModal from "./CriticalErrorModal.vue"

ChartJS.register(BarController, BarElement, CategoryScale, LinearScale)

export default { // JavaScript
  components: {
    GuideModal,
    SearchModal,
    PFPModal, 
    ExistingPlantModal,
    CriticalErrorModal
  },

	data() {
		return {
      activeModal: null, 
      errorMessage: null,

      //Placeholder moisture percentage
      moisture_percentage: 78,

      //Placeholder plant status: "good" | "warning" | "critical"
      plant_status: "good", 
		}
	},

	async mounted() {
    // Chart.js test - remove once verified
    new Chart(this.$refs.testChart, {
      type: "bar",
      data: {
        labels: ["A", "B", "C"],
        datasets: [{ label: "Test", data: [3, 7, 5] }]
      }
    })

    try {
      const res = await fetch ("/api/loremIpsum?wordCount=30")
      /*Broken Link:  http://thisdoesnotexist123456.com*/
      /*LIP:  /api/loremIpsum?wordCount=30*/
      /*DB port: uab420.desverreaux.com:8978/api/*/ 

      if (!res.ok) {
        throw new Error('HTTP error --> Status: ${res.status}')
      }

      this.moisture_percentage = 78

      if (this.moisture_percentage > 60) {
        this.plant_status = "good"
      } else if (this.moisture_percentage > 30) {
        this.plant_status = "warning"
      } else {
        this.plant_status = "critical"
      }

      const data = await res.json()

	  } catch (err) {
      console.log("Fetch Request Failed: ", err)

      this.errorMessage = err.message || "Unknown error"
      this.openModal("critical_error")
    }
  },
 
	methods: {
    openModal(name) {
      this.activeModal = name
      document.body.classList.add("no-scroll")
    },

    closeModal() {
      this.activeModal = null
      document.body.classList.remove("no-scroll")
    },

    //addPlant() {}
	}
}

</script>

<style> /* CSS */
/*
Evergreen - #0E2F15
Dark Spruce - #14591D
Dry Sage - #A6B07E
Smoky Rose - #8B635C
Firey Teracotta - #D1603D
*/
html, body, #app{
  width: 100%;
  margin: 0;
  padding: 0;
}

#app {
  max-width: none;
}

body {
  margin: 0;
}

.page {
  display: flex;
  flex-direction: column;

  height: 100vh; /*__vh = percentage of viewport height*/
  width: 100%;

	background-color: #14591D;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.title{
  font-family: "Merriweather";
  font-size: 4rem; 
  font-weight: bold; 
  font-style: oblique 10deg; 
  text-decoration: underline; 

  color: #a6b07e;
  cursor: default;
}

.UIElements {
  display: flex;
  gap: 1rem;
}

.Guide, .Search, .PFP {
  border-radius: 25px;
  background-color: #A6B07E;

  cursor: pointer;
  transition: background-color 0.2s ease;
}

.Guide:hover, .Search:hover, .PFP:hover{
  background-color: #7d855f;
}

.main {
  flex: 1;

  display: flex;
  justify-content: center;
  align-items: flex-start;

  gap: 2rem;
}

.plant_card {
  position: relative;

  width: 25%;
  height: 250px;

  background-color: #FFFFFF;
  border-radius: 25px;

  cursor: pointer;

  display: flex;
  justify-content: center;
  align-items: center;

  transition: background-color 0.2s ease;
}

.plant_card:hover {
  background-color: #dedbd5
}

.plant_icon {
  font-size: 7rem;
  color: #000000
}

.moisture_percentage {
  position: absolute;
  bottom: 10px;
  left: 10px;

  background-color: #000000;
  color: #FFFFFF;

  border-radius: 50%;

  width: 50px;
  height: 50px;

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: bold;
}

.status_icon {
  position: absolute;
  top: 10px;
  right: 10px;

  width: 40px; 
  height: 40px;

  border-radius: 50%;

  display: flex;
  align-items: center;
  justify-content: center;

  font-weight: bold;
}

.status_icon.good {
  background-color: #4CAF50;
  color: #FFFFFF;
}

.status_icon.warning {
  background-color: #FFC107;
  color: #000000;
}

.status_icon.critical {
  background-color: #F44336;
  color: #000000;
}


.new_plant{
  width: 25%;
  height: 250px;

  font-size: 7rem; 
  color: #5e5b53;

  background-color: #FFFFFF;  
  border-radius: 25px;

  cursor: pointer;

  transition: background-color 0.2s ease;
}

.new_plant:hover{
  background-color: #dedbd5;
}

.no-scroll {
  overflow: hidden;
}

/*
TO-DO:

Stretch:
 - Add scalability for smaller devices
*/
</style>


