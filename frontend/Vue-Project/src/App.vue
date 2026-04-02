<template> <!-- HTML -->
	<div class="page">
    <header class="header">
      <div class="title">Thirsty Plant</div>
      <div class="UIElements">
        <button class="Guide" @click="openModal('Guide')">Guide</button>
        <button class="Search" @click="openModal('Search')">Search</button>
        <button class="PFP" @click="openModal('PFP')">👤</button>
      </div>
    </header>
		
    <main class="main">
      <button class="existing_plant"@click="openModal('existing_plant')">🪴</button>
      <button class="new_plant" @click="openModal('new_plant')">+</button>
    </main>

    <!--Guide Modal-->
    <Modal :show="activeModal === 'Guide'" @close="closeModal">
      <h2>Plant Guide</h2>
      <p>Plant care guide and how to connect</p>
      <button @click="closeModal">X</button>
    </Modal>

    <!--Search Modal-->
    <Modal :show="activeModal === 'Search'" @close="closeModal">
      <h2>Search_______</h2>
      <input v-model="search_bar" placeholder="Search for plant" />
      <button @click="search_command">🔍</button>
      <button @click="closeModal">X</button>
    </Modal>

    <!--PFP Modal-->
    <Modal :show="activeModal === 'PFP'" @close="closeModal">
      <h2>User Profile</h2>
      <input v-model="user_name" placeholder="Username" />
      <button @click="update_profile">Update Profile</button>
      <button @click="closeModal">X</button>
    </Modal>
    
    <!--existing_plant Modal-->
    <Modal :show="activeModal === 'existing_plant'" @close="closeModal">
      <h2>Existing Plant</h2>
      <input v-model="search_bar" placeholder="Search for plant" />
      <textarea>This should say some text about your plant </textarea>
      <button @click="closeModal">X</button>
    </Modal>

    <!--new_plant Modal
    <Modal :show="activeModal === 'Search'" @close="closeModal">
      <h2>Search_______</h2>
      <input v-model="search_bar" placeholder="Search for plant" />
      <button @click="search_command">🔍</button>
      <button @click="closeModal">X</button>
    </Modal>  [IM NOT SURE YET IF THIS WILL BE NEEDED SINCE THIS ROUTES TO THE SEARCH FEATURE]-->
	</div>
</template>

<script>
import Modal from "./Modal.vue"

export default { // JavaScript
  components: {
    Modal
  },

	data() {
		return {
			message: "",
      activeModal: null, 
		}
	},

	async mounted() {
    try {
      const res = await fetch ("http://uab420.desverreaux.com:8000/api/loremIpsum?wordCount=30")
      const data = await res.json()
      this.message = data.message
      /* DB port: uab420.desverreaux.com:8978/api/*/ 
	  } catch (err) {
      console.log("Fetch Request Failed: ", err)
    }
  },
 
	methods: {
    openModal(name) {
      this.activeModal = name
      document.body.style.overflow = "hidden"
    },

    closeModal() {
      this.activeModal = null
      document.body.style.overflow = ""
    },

    //addPlant() {}

		changeMessage() {
			this.message = "Button Clicked"
		}
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
  font-size: 4rem; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  font-weight: bold; /*lighter, normal, bold, bolder*/
  font-style: oblique 10deg; /*normal, italic, etc*/
  text-decoration: underline; /*Can be customized*/

  color: #a6b07e;
  cursor: default;
}

.UIElements {
  display: flex;
  gap: 1rem;
}

.Guide {
  border-radius: 25px;
  background-color: #A6B07E;
  cursor: pointer;

  transition: background-color 0.2s ease;
}

.Guide:hover{
  background-color: #7d855f;
}

.Search {
  border-radius: 25px;
  background-color: #A6B07E;
  cursor: pointer;

  transition: background-color 0.2s ease;
}

.Search:hover{
  background-color: #7d855f;
}

.PFP {
  border-radius: 25px;
  background-color: #A6B07E;  
  cursor: pointer;
  color: #FFFFFF;

  transition: background-color 0.2s ease;

}

.PFP:hover{
  background-color: #7d855f;
}

.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: top;
  /*
  gap --> space between grid items
  padding --> space inside elements
  margin --> space outside elements
  */
}

/*textarea {
  width: 65%;
  height: 200px;
  font-size: 1rem;
  resize: none;
}*/

.existing_plant{ /* Note that this can be merged as .existing_plant, .new_plant{ */
  width: 25%;
  height: 250px;
  font-size: 7rem; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  

  background-color: #FFFFFF;
  border-radius: 25px;
  cursor: pointer;

  transition: background-color 0.2s ease;
}

.existing_plant:hover{
  background-color: #dedbd5;
}

.new_plant{
  width: 25%;
  height: 250px;
  font-size: 7rem; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  color: #5e5b53;

  background-color: #FFFFFF;  
  border-radius: 25px;
  cursor: pointer;

  transition: background-color 0.2s ease;
}

.new_plant:hover{
  background-color: #dedbd5;
}

/*
TO-DO:

Stretch:
 - Add scalability for smaller devices
*/
</style>


