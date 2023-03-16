<template>
<div>
  <v-parallax
      dark
      src="https://img.freepik.com/free-vector/nature-scene-with-river-hills-forest-mountain-landscape-flat-cartoon-style-illustration_1150-37326.jpg?w=1380&t=st=1678963146~exp=1678963746~hmac=bd54cafbc3035c0c91fa23e493dd05970be4eca63f1aa1bbe7d6c63db7143af5"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="text-h4 font-weight-thin mb-4">Forgot Password</h1>
          <h4 class="subheading">Welcome Build your application today!</h4>
        </v-col>
      </v-row>
    </v-parallax>
  <v-card :loading="loading" class="mx-auto my-12" max-width="374">
    <v-container class="justify-center">
      <template slot="progress">
        <v-progress-linear
          color="primary"
          height="10"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-card-title>Change Password</v-card-title>

      <v-card-text>
        <template>
          <ValidationObserver ref="observer" v-slot="{ invalid }">
            <form @submit.prevent="Pwd">
              <ValidationProvider
                name="E-mail"
                rules="required|email"
                v-slot="{ errors }"
                :bails="true"
              >
                <v-text-field
                  v-model="email"
                  type="email"
                  :messages="errors"
                  label="E-mail"
                  required
                  counter
                  outlined
                  shaped
                  prepend-icon="mdi-email"
                  hide-details="auto"
                />
              </ValidationProvider>

              <div>
                <v-spacer></v-spacer>
                <v-btn class="ma-4" text @click="Pwd" :disabled="invalid">
                  send it
                </v-btn>
              </div>
            </form>
          </ValidationObserver>
        </template>
      </v-card-text>
    </v-container>
  </v-card>
</div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import { required, email, min } from "vee-validate/dist/rules";
import { extend, setInteractionMode } from "vee-validate";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty"
});

extend("min", {
  ...min,
  message: "{_field_} may not be less than {length} characters"
});

extend("email", {
  ...email,
  message: "Email must be valid"
});

export default {
  data: () => ({
    email: "",
    loading: false,
    selection: 1
  }),

  methods: {
    Pwd() {
      this.$refs.observer.validate().then(success => {
        if (!success) {
          return;
        }

        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/auth/users/reset_password/",
          data: JSON.stringify({
            email: this.email
          }),
          headers: {
            "Content-Type": "application/json; charset=UTF-8"
          }
        })
          .then(res => {
            console.log(res);
            Vue.$cookies.remove("token");
            this.$router.push("/");
          })
          .catch(response => {
            console.log(response);
            alert(response);
            this.errored = true;
          });

        this.loading = true;
        setTimeout(() => (this.loading = false), 2000);
      });
    }
  }
};
</script>

<style></style>
