<template> <!-- HTML -->
	<div class="page">
    <header class="header">
      <div class="title">Thirsty Plant</div>
      <div class="UIElements">
        <span>Guide</span>
        <span>Search</span>
        <span>PFP</span>
      </div>
    </header>
    <button @click="guide">Guide</button>
		
    <main class="main">
      <textarea test={{ message }}></textarea>
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
			message: "Test Output"
		}
	},

	async mounted() {
		const res = await fetch ("http://uab420.desverreaux.com:8000/api/loremIpsum?wordCount=30")
		const data = await res.json()
		this.message = data.message
	},
 
	methods: {
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

.page {
  display: flex;
  flex-direction: column;
  height: 100vh; /*__vh = percentage of viewport height*/
  width: 95vh;
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

  color: #a6b07e
}

.UIElements {
  display: flex;
  gap: 1rem;
}

.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  /*
  gap --> space between grid items
  padding --> space inside elements
  margin --> space outside elements
  */
}

textarea {
  width: 65%;
  height: 200px;
  font-size: 1rem;
}

/*
TO-DO:

Stretch:
 - Add scalability for smaller devices
*/
</style>


