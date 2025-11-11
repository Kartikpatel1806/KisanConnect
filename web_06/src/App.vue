<template>
  <v-app>
    <div id="app">
      <div id="nav">
        <v-app-bar app color="#6495ED" dark>
          <div class="d-flex align-center">
            <v-img
              alt="Vuetify Logo"
              class="shrink mr-2"
              contain
              src="https://cdn.vuetifyjs.com/images/logos/vuetify-logo-dark.png"
              transition="scale-transition"
              width="40"
            />

            <v-card-text>
              <h1 class="appname">Fertilizer.io</h1>
            </v-card-text>
          </div>

          <v-spacer></v-spacer>

          <div v-if="isDisabled">
            <v-btn to="/" class="ma-1" color="#6495ED"> Home </v-btn>
            <span v-for="user in users" :key=user.id>
              <v-btn v-if="user.role=='farmer'" to="/crop" class="ma-1" color="#6495ED">
              Crop Recommendation
            </v-btn>
            <v-btn v-if="user.role=='farmer'" to="/fertilizer" class="ma-1" color="#6495ED">
              Fertilizer Recommendation
            </v-btn>
            </span>
            <v-btn to="/yield" class="ma-1" color="#6495ED"> yield Data </v-btn>
            <v-btn to="/account" class="ma-1" color="#6495ED">
              My Account
            </v-btn>
          </div>
          <v-btn to="/auth" class="ma-1" color="#6495ED" v-else> Login </v-btn>
        </v-app-bar>
      </div>
      <v-main>
        <router-view> </router-view>
      </v-main>
      <v-footer
        app
        bottom
        fixed
        class="justify-center"
        color="#292929"
        height="100"
      >
        <v-btn
          fab
          color="cyan accent-2"
          top
          right
          absolute
          @click="dialog = !dialog"
        >
          <v-icon>mdi-message</v-icon>
        </v-btn>
        <div
          class="title font-weight-light grey--text text--lighten-1 text-center"
        >
          &copy; {{ new Date().getFullYear() }} — Firtilize.io — Made by Our Team 
        </div>
      </v-footer>
    </div>

    <v-container>
      <template>
        <v-row justify="center">
          <v-dialog v-model="dialog" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Firtilize.io ChatBot</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-virtual-scroll
                    :items="messages_data"
                    item-height="200"
                    height="400"
                  >
                    <template v-slot:default="{ item }">
                      <div class="pa-10">
                        <v-textarea
                          :bench="benched"
                          :value="item.query"
                          :label="item.user_name"
                          outlined
                          readonly
                          auto-grow
                          rows="1"
                          prepend-icon="mdi-account"
                        >
                        </v-textarea>
                        <v-textarea
                          :value="item.answer"
                          label="BOT"
                          outlined
                          readonly
                          auto-grow
                          rows="2"
                          prepend-icon="mdi-robot-outline"
                        >
                        </v-textarea>
                      </div>
                    </template>
                  </v-virtual-scroll>
                  <v-row>
                    <v-col>
                      <v-textarea
                        auto-grow
                        rows="1"
                        v-model="question"
                        :append-outer-icon="
                          question ? 'mdi-send' : 'mdi-message'
                        "
                        :prepend-icon="icon"
                        filled
                        clear-icon="mdi-close-circle"
                        clearable
                        label="Message"
                        type="text"
                        @click:append-outer="sendMessage"
                        @click:prepend="changeIcon"
                        @click:clear="clearMessage"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="dialog = false">
                  Close
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </template>
      <template>
        <v-row justify="center">
          <v-dialog v-model="kyc_dialog" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Digital KYC</span>
              </v-card-title>
              <v-card-text>
                <div>
                  Notes: <br/>
                  1. Make sure to choose the right camera. <br/>
                  2. Make sure there is adequate lighting in the background. <br/>
                  3. Make sure your face is clearly visible. <br/>
                  4. Make sure the camera does not record multiple faces. <br/>
                  5. Normal blink eyes while recording video.
                </div>
                <div>
                  <recorderUI :videoTypes="['screen', 'camera']" />
                </div>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="kyc_dialog = false">
                  Close
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </template>
    </v-container>
  </v-app>
</template>

<script>
import Vue from "vue";
import axios from "axios";
import recorderUI from './components/kyc/recorderUI.vue';

export default {
  name: "App",
  components: {
    recorderUI
  },

  data: () => ({
    dialog: false,
    kyc_dialog: false,
    is_kyc: false,
    question: "",
    token: Vue.$cookies.get("token"),
    uid: Vue.$cookies.get("uid"),
    message: "",
    hint: [],
    iconIndex: 0,
    benched: 0,
    messages_data: null,
    users: "",
  }),
  computed: {
    isDisabled() {
      return Vue.$cookies.isKey("token");
    },
    items() {
      return Array.from({ length: this.length }, (k, v) => v + 1);
    },
    length() {
      return 7000;
    },
  },

  mounted() {
    if (Vue.$cookies.isKey("token")){
      this.GetMessage();
      this.Account();
    }
  },

  methods: {
    GetMessage() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/chatbot/",
        data: JSON.stringify({}),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          this.messages_data = res.data;
          console.log(this.messages_data);
        })
        .catch((error) => {
          alert(error);
          this.errored = true;
        });
    },

    sendMessage() {
      this.SendMessage();
      this.resetIcon();
      this.clearMessage();
    },
    clearMessage() {
      this.message = "";
    },
    resetIcon() {
      this.iconIndex = 0;
    },
    changeIcon() {
      this.iconIndex === this.icons.length - 1
        ? (this.iconIndex = 0)
        : this.iconIndex++;
    },

    SendMessage() {
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/chatbot/",
        data: {
          question: this.question,
        },
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res);
          alert("Thanks for you query!");
          window.location.reload();
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
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
          this.users = res.data
          const users = res.data;
          const is_kyc = users[0].is_kyc;
          if (!is_kyc) {
            this.kyc_dialog = true;
            console.log(is_kyc, this.kyc_dialog);
            Vue.$cookies.set("uid", users[0].id);
          }
        })
        .catch((error) => {
          alert(error);
          this.errored = true;
        });
    },
  },
};
</script>

<style>
.appname {
  padding-top: 20px;
  font-size: 20px;
  color: black;
}

h1 {
  font-weight: 800;
  font-size: 18px;
  letter-spacing: 4px;
  margin: 0 0 1em 0;
  text-transform: uppercase;
}

h2 {
  margin: 0 0 1em 0;
  line-height: 22px;
  letter-spacing: 2px;
  font-size: 14px;
  font-weight: 800;
  text-transform: uppercase;
}

h3 {
  margin: 0 0 1em 0;
  letter-spacing: 2px;
  line-height: 22px;
  font-size: 16px;
  font-weight: 800;
  text-transform: uppercase;
}

p {
  line-height: 22px;
  margin: 0 0 1em 0;
  font-size: 18px;
  /* color: #303030; */
}
.contact-line {
  display: flex;
  margin: 0 auto;
  align-items: center;
}
.contact {
  padding-left: 1em;
  margin: 0.25em;
}
.experience-section {
  margin-bottom: 2em;
}
.experience-section:last-child {
  margin-bottom: 0;
}
.work-position-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.education-section {
  margin-bottom: 2em;
}
.education-section:last-child {
  margin-bottom: 0;
}
.chart {
  text-align: center;
  font-size: 12px;
  padding: 0px;
  margin: 0px;
}
.dates {
  margin: 0 0 1em 0;
  line-height: 22px;
  letter-spacing: 0px;
  font-size: 14px;
  font-weight: 900;
  text-transform: uppercase;
  color: #87ceeb;
}
</style>
