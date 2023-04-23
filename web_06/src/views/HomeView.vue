<template>
  <div class="home">
        <v-parallax
      dark
      src="https://cdn.vuetifyjs.com/images/parallax/material2.jpg"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="text-h4 font-weight-thin mb-4"> Make your life healthier </h1>
          <h4 class="subheading">Now directly purchase from farmers & eat organic!</h4>
        </v-col>
      </v-row>
    </v-parallax>
    <AboutView />
  </div>
</template>

<script>
import AboutView from './AboutView.vue'
export default {
  name: 'HomeView',
  components: {
    AboutView,
  }
}
</script>
