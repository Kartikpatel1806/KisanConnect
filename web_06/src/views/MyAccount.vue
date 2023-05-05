<template>
  <div class="doctorslist">
    <v-container class="text-center">
      <h1>My Account</h1>

      <v-responsive class="mx-auto mb-12" width="56">
        <v-divider class="mb-1"></v-divider>

        <v-divider></v-divider>
      </v-responsive>

      <v-row v-for="user in users" :key="user.id">
        <v-col cols="12" md="4">
          <v-card class="py-12 px-4" color="grey lighten-5" flat elevation="14" shaped>
            <v-card-title
              class="justify-center font-weight-black text-uppercase"
            >
              {{ user.name }}
            </v-card-title>

            <v-theme-provider dark>
              <div>
                <p>Email: {{ user.email }}</p>
                <p v-if="user.is_superuser">Role: Admin</p>
                <p v-else>Role: {{ user.role }}</p>
                <p v-if="user.is_kyc">KYC Status: Done</p>
                <p v-else>KYC Status: Not completed yet</p>
              </div>
            </v-theme-provider>

            <v-card-text>
              <v-btn to="/auth/change-password"> Change Password </v-btn>
              <v-btn @click="Logout" class="ma-1"> Logout </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";
export default {
  data: () => ({
    first_name: "",
    last_name: "",
    email: "",
    users: "",
    token: Vue.$cookies.get("token"),
    role: Vue.$cookies.get("role"),
  }),

  computed: {
    isDisabled() {
      return Vue.$cookies.isKey("token");
    },
  },

  mounted () {
   this.Account()
},
  
  methods: {
    Logout() {
      Vue.$cookies.remove("token");
      localStorage.removeItem("app_id")
      this.$router.push("/auth");
      window.location.reload();
    },

    Account() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/user/",
        data: JSON.stringify({}),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          this.users = (res.data)
          console.log(this.users[0].role);
          Vue.$cookies.set("role", this.users[0].role);
        })
        .catch((error) => {
          alert(error);
          this.errored = true;
        });
    },
  },
};
</script>
