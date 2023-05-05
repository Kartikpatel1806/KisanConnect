<template>
  <div>
    <v-simple-table fixed-header>
      <template v-slot:default>
        <thead>
          <tr>
            <th class="text-left">User Name</th>
            <th class="text-left">Question</th>
            <th class="text-left">Answer</th>
            <th class="text-left">Answer the Query</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in datas" :key="item.id">
            <td>{{ item.user_name }}</td>
            <td>{{ item.description }}</td>
            <td>
                <img
                  :src="`http://127.0.0.1:8000/` + item.image"
                  height="200"
                  width="200"
                />
            </td>
            <td>
              <v-btn
                dark
                text
                color="primary"
                class="ml-2"
                @click="SaveData(item.id)"
              >
                <v-icon>mdi-pen</v-icon>
              </v-btn>
              <v-btn
                dark
                text
                color="primary"
                class="ml-2"
                @click="DeleteData(item.id)"
              >
                <v-icon>mdi-delete</v-icon>
              </v-btn>
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>

    <template>
      <v-row justify="center">
        <v-dialog v-model="dialog" persistent max-width="600px">
          <v-card>
            <v-card-title>
              <span class="text-h5">User Profile</span>
            </v-card-title>
            <v-card-text>
              <v-textarea
                v-model="answer"
                type="text"
                :counter="1500"
                label="Answer"
                required
                dense
                filled
                auto-grow
                rows="2"
                hide-details="auto"
              />
            </v-card-text>
            <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn color="blue darken-1" text @click="dialog = false">
                Close
              </v-btn>
              <v-btn color="blue darken-1" text @click="Submit()"> Save </v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
      </v-row>
    </template>
  </div>
</template>

<script>
import Vue from "vue";
import axios from "axios";

export default {
  data: () => ({
    answer: "",
    datas: "",
    dialog: false,
    question_id: null,
    items: "",
    token: Vue.$cookies.get("token"),
    admin: Vue.$cookies.get("admin"),
  }),

  mounted() {
    this.Get();
  },

  methods: {
    SaveData(id) {
      this.dialog = true;
      this.question_id = id;
      console.log(this.question_id);
    },
    Submit() {
      axios({
        method: "PUT",
        url: "http://127.0.0.1:8000/chat/",
        data: {
          answer: this.answer,
          id: this.question_id,
        },
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res);
          alert("Thanks for your reply!");
          window.location.reload();
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },

    Get() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/yield/",
        data: JSON.stringify({
          state: this.state,
        }),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
            this.items = res.data
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },

    GetQuery() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/chat/?is_admin=" + this.admin,
        data: JSON.stringify({}),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          this.datas = res.data;
          console.log(this.datas);
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },

    DeleteData(id) {
      this.question_id = id;
      console.log(this.question_id);
      this.Delete()
    },
    Delete() {
      axios({
        method: "DELETE",
        url: "http://127.0.0.1:8000/bot/",
        data: {
          id: this.question_id,
        },
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res);
          alert("Message is successfully deleted!");
          window.location.reload();
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },
  },
};
</script>
