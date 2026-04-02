<template> <!-- HTML -->
	<div class="page">
    <header class="header">
      <div class="title">Thirsty Plant</div>
      <div class="UIElements">
        <button class="Guide" @click="changeMessage">Guide</button>
        <button class="Search">Search</button>
        <button class="PFP">PFP</button>
      </div>
    </header>
		
    <main class="main">
      <!--<textarea :value="message"></textarea>-->
      <button class="existing_plant">🪴</button>
      <button class="new_plant">+</button>

      <!--
      <section class="main">{{ message }}</section>
		  <button @click="changeMessage">Change Message</button>
       <aside class="sidebar">Your Ad Here!</aside>
       -->
    </main>
	</div>
</template>

<script>

export default { // JavaScript
	data() {
		return {
			/*message: "Test Output"*/
		}
	},

	async mounted() {
		const res = await fetch ("http://uab420.desverreaux.com:8000/api/loremIpsum?wordCount=30")
		const data = await res.json()
		this.message = data.message
	},
 
	methods: {
		changeMessage() {
			this.textarea = "Button Clicked"
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
}

.Search {
  border-radius: 25px;
  background-color: #A6B07E;
  cursor: pointer;
}

.PFP {
  border-radius: 25px;
  background-color: #A6B07E;  
  cursor: pointer;
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

.existing_plant{
  width: 25%;
  height: 250px;
  font-size: 7rem; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  

  background-color: #FFFFFF;
  border-radius: 25px;
  cursor: pointer;
}

.new_plant{
  width: 25%;
  height: 250px;
  font-size: 7rem; /* pm = pixels, em/% = relative to parent element (default is 1em = 16px), rem = relative to html element --> Can also use xx-small to xx-large*/
  color: #5e5b53;

  background-color: #FFFFFF;  
  border-radius: 25px;
  cursor: pointer;
}

/*
TO-DO:

Stretch:
 - Add scalability for smaller devices
*/
</style>


