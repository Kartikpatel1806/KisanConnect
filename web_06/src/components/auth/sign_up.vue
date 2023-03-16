<template>
  <div>
    <v-parallax
      dark
      src="https://img.freepik.com/free-vector/nature-scene-with-river-hills-forest-mountain-landscape-flat-cartoon-style-illustration_1150-37326.jpg?w=1380&t=st=1678963146~exp=1678963746~hmac=bd54cafbc3035c0c91fa23e493dd05970be4eca63f1aa1bbe7d6c63db7143af5"
    >
      <v-row align="center" justify="center">
        <v-col class="text-center" cols="12">
          <h1 class="text-h4 font-weight-thin mb-4">Register</h1>
          <h4 class="subheading">Welcome make your life easier with us!</h4>
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

        <v-card-title>Join us</v-card-title>
        <v-card-subtitle> Enter your details </v-card-subtitle>

        <v-card-text>
          <template>
            <ValidationObserver ref="observer" v-slot="{ invalid }">
              <form @submit.prevent="Signup">
                <ValidationProvider
                  name="E-mail"
                  rules="required|email"
                  v-slot="{ errors }"
                >
                  <v-text-field
                    v-model="email"
                    type="email"
                    label="E-mail"
                    required
                    counter
                    outlined
                    shaped
                    :error-messages="errors"
                    prepend-icon="mdi-email"
                    hide-details="auto"
                  />
                </ValidationProvider>

                <ValidationProvider
                  name="First-Name"
                  rules="required|max:30"
                  v-slot="{ errors }"
                >
                  <v-text-field
                    v-model="fullName"
                    type="text"
                    :counter="30"
                    label="Full Name"
                    required
                    outlined
                    shaped
                    :error-messages="errors"
                    prepend-icon="mdi-account"
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
                    label="Password"
                    required
                    counter
                    outlined
                    shaped
                    :error-messages="errors"
                    :append-icon="show1 ? 'mdi-eye' : 'mdi-eye-off'"
                    :type="show1 ? 'text' : 'password'"
                    @click:append="show1 = !show1"
                    prepend-icon="mdi-lock"
                    hide-details="auto"
                  />
                </ValidationProvider>

                <v-btn
                  class="mr-4"
                  type="Signup"
                  text
                  @click="reserve"
                  :disabled="invalid"
                >
                  Register
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
import axios from "axios";
import { required, email, min, max } from "vee-validate/dist/rules";
import { extend, setInteractionMode } from "vee-validate";

setInteractionMode("eager");

extend("required", {
  ...required,
  message: "{_field_} can not be empty",
});

extend("min", {
  ...min,
  message: "{_field_} may not be less than {length} characters",
});

extend("max", {
  ...max,
  message: "{_field_} may not be more than {length} characters",
});

extend("email", {
  ...email,
  message: "Email must be valid",
});

export default {
  data: () => ({
    email: "",
    fullName: "",
    password: "",
    token: "",
    loading: false,
    show1: false,
    show2: false,
    is_valid: false,
  }),

  methods: {
    verifyMethod(response) {
      console.log(response);
      this.is_valid = true;
    },

    errorMethod(response) {
      console.log(response);
    },

    Signup() {
      this.$refs.observer.validate().then((success) => {
        if (!success) {
          return;
        }

        axios({
          method: "POST",
          url: "http://127.0.0.1:8000/auth/users/",
          data: JSON.stringify({
            email: this.email,
            name: this.fullName,
            password: this.password,
          }),
          headers: {
            "Content-Type": "application/json; charset=UTF-8",
          },
        })
          .then((res) => {
            console.log(res);
            this.$router.push("/auth");
          })
          .catch((error) => {
            alert(error);
            this.errored = true;
          });

        this.loading = true;
        setTimeout(() => (this.loading = false), 2000);
      });
    },
  },
};
</script>

<style></style>
