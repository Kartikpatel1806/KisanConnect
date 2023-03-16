<template>
<div>
  <v-parallax
      dark
      src="https://img.freepik.com/free-vector/nature-scene-with-river-hills-forest-mountain-landscape-flat-cartoon-style-illustration_1150-37326.jpg?w=1380&t=st=1678963146~exp=1678963746~hmac=bd54cafbc3035c0c91fa23e493dd05970be4eca63f1aa1bbe7d6c63db7143af5"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="text-h4 font-weight-thin mb-4">Change Password</h1>
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

      <v-card-title>Change Password</v-card-title>
      <v-card-subtitle>
        Make Sure you have entered correct credentials
      </v-card-subtitle>

      <v-card-text>
        <template>
          <ValidationObserver ref="observer" v-slot="{ invalid }">
            <form @submit.prevent="Login">
              <ValidationProvider
                name="OldPassword"
                rules="required|min:8"
                v-slot="{ errors }"
              >
                <v-text-field
                  v-model="old"
                  label="Old Password"
                  required
                  counter
                  outlined
                  shaped
                  :messages="errors"
                  :append-icon="show3 ? 'mdi-eye' : 'mdi-eye-off'"
                  :type="show3 ? 'text' : 'password'"
                  @click:append="show3 = !show3"
                  prepend-icon="mdi-lock"
                  hide-details="auto"
                />
              </ValidationProvider>

              <ValidationProvider
                name="Password"
                rules="required|min:8"
                v-slot="{ errors }"
              >
                <v-text-field
                  v-model="password"
                  label="New Password"
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
                Change Password
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
    old: "",
    password: "",
    confirmation: "",
    loading: false,
    selection: 1,
    show1: false,
    show2: false,
    show3: false,
    token: Vue.$cookies.get("token")
  }),

  methods: {
    Login() {
      this.$refs.observer.validate().then(success => {
        if (!success) {
          return;
        }

        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/auth/users/set_password/",
          data: JSON.stringify({
            new_password: this.password,
            current_password: this.old
          }),
          headers: {
            "Content-Type": "application/json; charset=UTF-8",
            "Authorization": `token ${this.token}`
          }
        })
          .then(res => {
            Vue.$cookies.remove("token");
            console.log(res);
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
