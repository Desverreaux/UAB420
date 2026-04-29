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
          class="Search"
          @click="openModal('Search')">Search
        </button>

        <a 
          class="Database"
          href="http://uab420.desverreaux.com:8978" 
          target="_blank" 
          rel="noopener">Database
        </a> 

        <button
          class="Profile"
          @click="openModal('Profile')">👤
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

      <button 
        class="new_plant"
        @click="openModal('new_plant')">+
      </button>

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

      //Placeholder moisture percentage
      moisture_percentage: 78,

      //Placeholder plant status: "good" | "warning" | "critical"
      plant_status: "good", 

		}
	},

	async mounted() {
    try {
      const res = await fetch ("/api/loremIpsum?wordCount=30")
      /*Broken Link:  http://thisdoesnotexist123456.com*/
      /*LIP:  /api/loremIpsum?wordCount=30*/
      /*DB port: uab420.desverreaux.com:8978/api/*/ 

      if (!res.ok) {
        throw new Error(`HTTP error --> Status: ${res.status}`)
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

.chart_card {
  width: 50%;
  background-color: #FFFFFF;
  border-radius: 25px;
  padding: 1.5rem;
  margin-top: 1rem;
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


