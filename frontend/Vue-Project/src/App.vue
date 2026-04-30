<template> <!-- HTML -->
	<div class="page">
    <header class="header">
      <img 
        src="/src/assets/Images/graphic_design_is_my_passion2.png"
        alt="Thirsty Plant Logo"
        class="logo"
      />

      <div class="UIElements">
        <button 
          class="Guide"
          @click="openModal('Guide')">Guide
        </button>

        <button 
          class="Database"
          @click="openDatabase">
          Database
        </button> 

        <button
          class="Profile"
          @click="openModal('Profile')">👤
        </button>

      </div>
    </header>
		
    <main class="main">
      <div v-for="plant in plant_cards" :key="plant.id" class="plant_card" @click="openPlantModal(plant)">

        <div v-if="plant.isProbe" class="status_icon" :class="plant.status">
          <span v-if="plant.status === 'good'">✓</span>
          <span v-else-if="plant.status === 'warning'">⚠️</span>
          <span v-else>!</span>
        </div>

        <div class="plant_icon">🪴</div>

        <div v-if="plant.isProbe" class="moisture_percentage"> {{ plant.moisture }}% </div>

        <div v-else class = "demo_plant_label">Demo Plant</div>

      </div>

      <button class="new_plant" @click="addDemoPlant">+</button>

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

    <!--Profile Modal-->
    <ProfileModal 
      :show="activeModal === 'Profile'" 
      @close="closeModal"
    />
    
    <!--existing_plant Modal-->
    <ExistingPlantModal 
      :show="activeModal === 'existing_plant'" 
      :plant="selectedPlant"
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
import GuideModal from "./GuideModal.vue"
import SearchModal from "./SearchModal.vue"
import ProfileModal from "./ProfileModal.vue"
import ExistingPlantModal from "./ExistingPlantModal.vue"
import CriticalErrorModal from "./CriticalErrorModal.vue"

export default { // JavaScript
  components: {
    GuideModal,
    SearchModal,
    ProfileModal, 
    ExistingPlantModal,
    CriticalErrorModal,
  },

	data() {
		return {
      activeModal: null, 
      errorMessage: null,
      selectedPlant: null, 

      plant_cards: [
        {
          id: 1,
          name: "Soil Probe Plant",
          isProbe: true,
          moisture: 78,
          status: "good",
          graphLabels: [],
          graphData: []
        }
      ],

      moistureInterval: null

		}
	},

	async mounted() {
    await this.fetchProbePlantData()

    this.moistureInterval = setInterval(this.fetchProbePlantData, 5000)
    },

    beforeUnmount() {
      clearInterval(this.moistureInterval)
    },

    
 
	methods: {
    async fetchProbePlantData() {
      try {
        const probePlant = this.plant_cards.find(plant => plant.isProbe)

        if (!probePlant) return

        const res = await fetch(`/api/getHistoricalData?plantIdentifier=${probePlant.id}`)

        if (!res.ok) {
          throw new Error(`HTTP error --> Status: ${res.status}`)
        }

        const result = await res.json()

        let readingsObject = result.data || {}

        if (typeof readingsObject === "string") {
          readingsObject = JSON.parse(readingsObject)
        }

        const readingsArray = Object.values(readingsObject)
          .filter(reading => reading && reading.reading_at && reading.moistureLevel !== undefined)

        if (readingsArray.length === 0) {
          throw new Error("No valid moisture readings found")
        }

        readingsArray.sort((a, b) => {
          return new Date(a.reading_at) - new Date(b.reading_at)
        })

        const latestReading = readingsArray[readingsArray.length - 1]

        const moisturePercent = Math.round(Number(latestReading.moistureLevel) * 100)

        probePlant.moisture = moisturePercent
        probePlant.status = this.getPlantStatus(moisturePercent)

      } catch (err) {
        console.log("Fetch Request Failed: ", err)

        this.errorMessage = err.message || "Unknown error"
        this.openModal("critical_error")
      }
    },

    getPlantStatus(moisturePercent) {
      if (moisturePercent > 60) {
        return "good"
      } else if (moisturePercent > 30) {
        return "warning"
      } else {
        return "critical"
      }
    },

    addDemoPlant() {
      const demoPlantNumber = this.plant_cards.length
      const demoGraph = this.generateSmoothDemoMoistureData()

      this.plant_cards.push({
        id: `demo-plant-${Date.now()}`,
        name: `Demo Plant ${demoPlantNumber}`,
        isProbe: false,
        moisture: null,
        status: null,
        graphLabels: demoGraph.labels,
        graphData: demoGraph.data
      })
    },

    generateSmoothDemoMoistureData() {
      const labels = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

      let currentMoisture = Math.floor(Math.random() * 31) + 45
      const data = []

      for (let i = 0; i < labels.length; i++) {
        const change = Math.floor(Math.random() * 11) - 5

        currentMoisture += change

        if (currentMoisture > 90) currentMoisture = 90
        if (currentMoisture < 20) currentMoisture = 20

        data.push(currentMoisture)
      }

      return {
        labels, 
        data
      }
    },

    openPlantModal(plant) {
      this.selectedPlant = plant
      this.openModal("existing_plant")
    },

    openModal(name) {
      this.activeModal = name
      document.body.classList.add("no-scroll")
    },

    closeModal() {
      this.activeModal = null
      document.body.classList.remove("no-scroll")
    },

    openDatabase() {
      const url = "http://uab420.desverreaux.com:8978"
      const newTab = window.open(url, "_blank")

      if (!newTab) {
        window.location.href = url
      }
    }

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

  background-image: url("/src/assets/Images/leaf-pattern.svg");

  background-size: 80px;

  background-repeat: repeat;

  background-blend-mode: soft-light;
}

.logo {
  height: 150px;
  width: auto;
  object-fit: contain;
  cursor: default;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem;
}

.UIElements {
  display: flex;
  gap: 1rem;
}

.Guide, .Search, .Profile, .Database {
  border-radius: 25px;
  background-color: #A6B07E;
  color: #000000;

  cursor: pointer;
  transition: background-color 0.2s ease;
}

.Guide:hover, .Search:hover, .Profile:hover, .Database:hover{
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

.demo_plant_label {
  position: absolute;
  bottom: 15px;

  color: #0E2F15;
  font-weight: bold;
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
 - Title: 
    - The site is still showing the original logo. 
    - [Q]: Cecil it looked like you had added it, was that in your branch specifically or just overlaid on an image?
      - If not, if youll send me that file and ill figure out how to add it in. 

 - Plant Card:
    - Left Corner --> Need to use fetch to live-update moisture percentage
    - Right Corner --> Need to use the fetched moisture update to change the status icon
    - On Click:
      - The graph is pulling dummy data from the backend but nothing is populating. [Q]: Do we want the site to pull dummy data for demo purposes? Or do we wanna go ahead and modify to pull real data?
      - I still need to format the graph to stay within the modal.
    
 - New Plant:
    - Currently does nothing, but im gonna add functionality. The new plants will not have moisture or status icons. The graphs within will use purely dummy data that ill hardcode.
    - [Q]: Seth if you can type out an improved guide since youre knowledgeable about the probe?

 - Search:
    - There is no database of plants, so this is currently useless.
    - [Q]: Do we want to try to add a plant database, or scrap the feature entirely?

 - Database button needs to be removed. LET ME KNOW WHEN TO DO SO

 - Profile:
    - Currently doesnt do much, but I can set it up such that the true plant card uses dummy data until logged in, and uses real data afterwards. I'd also change the modal to show some logged in status.
    - The login button is currently NOT linked to the database. I also need to add functionality for new users.
*/
</style>


