<template>
  <div class="home">
        <v-parallax
      dark
      src="https://img.freepik.com/free-vector/nature-scene-with-river-hills-forest-mountain-landscape-flat-cartoon-style-illustration_1150-37326.jpg?w=1380&t=st=1678963146~exp=1678963746~hmac=bd54cafbc3035c0c91fa23e493dd05970be4eca63f1aa1bbe7d6c63db7143af5"
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
