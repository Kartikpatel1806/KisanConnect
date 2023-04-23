<template>
<div>
  <v-parallax
      dark
      src="https://cdn.vuetifyjs.com/images/parallax/material2.jpg"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="text-h4 font-weight-thin mb-4">Reset Password</h1>
          <h4 class="subheading">Welcome Build your application today!</h4>
        </v-col>
      </v-row>
    </v-parallax>
  <v-card :loading="loading" class="mx-auto my-12" max-width="374">
    <v-container class="justify-center">
      <template slot="progress">
        <v-progress-linear
          color="deep-purple"
          height="10"
          indeterminate
        ></v-progress-linear>
      </template>

      <v-card-title>Join us</v-card-title>
      <v-card-subtitle>
        Join us with over 5million+ Heart Cure Patients
      </v-card-subtitle>

      <v-card-text>
        <template>
          <ValidationObserver ref="observer" v-slot="{ invalid }">
            <form @submit.prevent="Login">
              <ValidationProvider
                name="Password"
                rules="required|min:8"
                v-slot="{ errors }"
              >
                <v-text-field
                  v-model="password"
                  label="Password"
                  required
                  counter
                  outlined
                  shaped
                  :messages="errors"
                  :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show1 ? 'text' : 'password'"
                  @click:append="show1 = !show1"
                  prepend-icon="mdi-lock"
                  hide-details="auto"
                />
              </ValidationProvider>

              <ValidationProvider
                name="Confirm-Password"
                rules="required|min:8"
                v-slot="{ errors }"
              >
                <v-text-field
                  v-model="confirmation"
                  label="Confirm Password"
                  required
                  counter
                  outlined
                  shaped
                  :messages="errors"
                  :append-icon="show2 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show2 ? 'text' : 'password'"
                  @click:append="show2 = !show2"
                  prepend-icon="mdi-lock"
                  hide-details="auto"
                />
              </ValidationProvider>

              <v-spacer></v-spacer>

              <v-btn
                class="mr-4"
                type="Login"
                text
                @click="reserve"
                :disabled="invalid"
              >
                Reset Password
              </v-btn>
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
    password: "",
    confirmation: "",
    uid: "",
    token: "",
    loading: false,
    selection: 1,
    show1: false,
    show2: false
  }),

  methods: {
    Login() {
      this.$refs.observer.validate().then(success => {
        if (!success) {
          return;
        }

        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/auth/users/reset_password_confirm/",
          data: JSON.stringify({
            uid: this.$route.params.uid,
            token: this.$route.params.token,
            new_password: this.password
          }),
          headers: {
            "Content-Type": "application/json; charset=UTF-8"
          }
        })
          .then(res => {
            console.log(res);
            Vue.$cookies.remove("token");
            this.$router.push("/auth");
          })
          .catch(error => {
            alert(error);
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
