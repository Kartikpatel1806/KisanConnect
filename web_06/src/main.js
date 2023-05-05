import Vue from 'vue'
import App from './App.vue'
import router from './router'
import vuetify from './plugins/vuetify'
import { ValidationProvider, ValidationObserver } from "vee-validate";
import VueCookies from "vue-cookies";
import { RecorderView } from './components/kyc/RecorderView.vue';

Vue.use(VueCookies);
Vue.component("ValidationProvider", ValidationProvider);
Vue.component("ValidationObserver", ValidationObserver);
Vue.component("RecorderView", RecorderView)


Vue.config.productionTip = false

new Vue({
  router,
  vuetify,
  render: h => h(App)
}).$mount('#app')
