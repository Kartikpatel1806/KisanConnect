<template>
  <v-container fluid>
    <div v-if="role == 'farmer'">
      <v-btn dark text color="primary" class="ml-2" @click="CreatePost()">
        Post Yield
      </v-btn>
    </div>

    <v-container>
      <template>
        <v-row justify="center">
          <v-dialog v-model="create_post_dialog" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Post Crop Yield</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col>
                      <v-file-input
                        v-model="images"
                        accept="image/png, image/jpeg, image/bmp, image/jpg"
                        placeholder="Pick an Image"
                        prepend-icon="mdi-camera"
                      ></v-file-input>

                      <v-textarea
                        v-model="description"
                        label="Discription"
                        type="text"
                      ></v-textarea>
                    </v-col>
                  </v-row>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="blue darken-1"
                  text
                  @click="create_post_dialog = false"
                >
                  Close
                </v-btn>
                <v-btn color="blue darken-1" text @click="SavePost()">
                  Save
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </template>

      <template>
        <v-row justify="center">
          <v-dialog v-model="chat_dialog" persistent max-width="600px">
            <v-card>
              <v-card-title>
                <span class="text-h5">Chat with seller</span>
              </v-card-title>
              <v-card-text>
                <v-container>
                  <v-virtual-scroll
                :items="datas"
                item-height="80"
                height="300"
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
                  </div>
                </template>
                  </v-virtual-scroll>
                  <v-row>
                    <v-text-field
                      v-model="query"
                      label="Ask Query"
                      type="text"
                    ></v-text-field>
                  </v-row>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" text @click="chat_dialog = false">
                  Close
                </v-btn>
                <v-btn color="blue darken-1" text @click="Bot()"> Save </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </template>
      
      <template>
        <v-row justify="center">
          <v-dialog v-model="delete_dialog" persistent max-width="400px">
            <v-card>
              <v-card-title class="text-h5">
                Confirm Delete
              </v-card-title>
              <v-card-text>
                Are you sure you want to delete this yield? This action cannot be undone.
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="grey darken-1" text @click="delete_dialog = false">
                  Cancel
                </v-btn>
                <v-btn color="error darken-1" text @click="DeleteYield()">
                  Delete
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-row>
      </template>
    </v-container>
    <v-data-iterator
      :items="items"
      :items-per-page.sync="itemsPerPage"
      :page.sync="page"
      :search="search"
      :sort-by="sortBy.toLowerCase()"
      :sort-desc="sortDesc"
      hide-default-footer
    >
      <template v-slot:header>
        <v-toolbar dark color="blue darken-3" class="mb-1">
          <v-text-field
            v-model="search"
            clearable
            flat
            solo-inverted
            hide-details
            prepend-inner-icon="mdi-magnify"
            label="Search"
          ></v-text-field>
          <template v-if="$vuetify.breakpoint.mdAndUp">
            <v-spacer></v-spacer>
            <v-btn-toggle v-model="sortDesc" mandatory>
              <v-btn large depressed color="blue" :value="false">
                <v-icon>mdi-arrow-up</v-icon>
              </v-btn>
              <v-btn large depressed color="blue" :value="true">
                <v-icon>mdi-arrow-down</v-icon>
              </v-btn>
            </v-btn-toggle>
          </template>
        </v-toolbar>
      </template>

      <template v-slot:default="props">
        <v-row>
          <v-col
            v-for="item in props.items"
            :key="item.name"
            cols="12"
            sm="6"
            md="4"
            lg="3"
          >
            <v-card>
              <v-card-title class="subheading font-weight-bold justify-center">
                <img
                  v-if="item.image"
                  :src="item.image"
                  height="200"
                  width="200"
                  style="object-fit: cover;"
                  alt="Yield Image"
                />
                <v-icon v-else size="100" color="grey lighten-1">mdi-image-off</v-icon>
              </v-card-title>

              <v-divider></v-divider>

              <v-list dense>
                <v-list-item>
                  <v-list-item-content
                    class="justify-center"
                    :class="{ 'blue--text': sortBy === key }"
                  >
                    <br />
                    <p>{{ item.description }}</p>

                    <div v-if="!item.is_sold">
                      <v-btn text color="error" @click="ChatDialog(item.id)">
                        Chat with seller
                      </v-btn>
                    </div>
                    
                    <div v-if="isOwner(item.user_id)" class="mt-2">
                      <v-btn 
                        text 
                        color="error" 
                        small
                        @click="confirmDelete(item.id)"
                      >
                        <v-icon small left>mdi-delete</v-icon>
                        Delete
                      </v-btn>
                    </div>
                  </v-list-item-content>
                </v-list-item>
              </v-list>
            </v-card>
          </v-col>
        </v-row>
      </template>

      <template v-slot:footer>
        <v-row class="mt-2" align="center" justify="center">
          <span class="grey--text">Items per page</span>
          <v-menu offset-y>
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                dark
                text
                color="primary"
                class="ml-2"
                v-bind="attrs"
                v-on="on"
              >
                {{ itemsPerPage }}
                <v-icon>mdi-chevron-down</v-icon>
              </v-btn>
            </template>
            <v-list>
              <v-list-item
                v-for="(number, index) in itemsPerPageArray"
                :key="index"
                @click="updateItemsPerPage(number)"
              >
                <v-list-item-title>{{ number }}</v-list-item-title>
              </v-list-item>
            </v-list>
          </v-menu>

          <v-spacer></v-spacer>

          <span class="mr-4 grey--text">
            Page {{ page }} of {{ numberOfPages }}
          </span>
          <v-btn
            fab
            dark
            color="blue darken-3"
            class="mr-1"
            @click="formerPage"
          >
            <v-icon>mdi-chevron-left</v-icon>
          </v-btn>
          <v-btn fab dark color="blue darken-3" class="ml-1" @click="nextPage">
            <v-icon>mdi-chevron-right</v-icon>
          </v-btn>
        </v-row>
      </template>
    </v-data-iterator>
  </v-container>
</template>

<script>
import Vue from "vue";
import axios from "axios";

export default {
  data() {
    return {
      token: Vue.$cookies.get("token"),
      state: Vue.$cookies.get("states"),
      itemsPerPageArray: [50, 100],
      search: "",
      filter: {},
      sortDesc: false,
      page: 1,
      itemsPerPage: 50,
      sortBy: "title",
      keys: [
        "title",
        "description",
        "weight",
        "created_at",
        "expires_at",
        "image",
      ],
      items: [],
      create_post_dialog: false,
      chat_dialog: false,
      delete_dialog: false,
      delete_yield_id: null,
      description: "",
      is_sold: false,
      images: [],
      query: "",
      uid: "",
      datas: "",
      role: Vue.$cookies.get("role"),
      currentUserId: parseInt(Vue.$cookies.get("uid")) || null,
      
    hint: [],
    iconIndex: 0,
    benched: 0,
    messages_data: null,
    };
  },
  computed: {
    numberOfPages() {
      return Math.ceil(this.items.length / this.itemsPerPage);
    },
    filteredKeys() {
      return this.keys.filter((key) => key !== "Description");
    },
  },
  mounted() {
    this.Get();
    // Ensure currentUserId is set from cookies
    const uid = Vue.$cookies.get("uid");
    if (uid) {
      this.currentUserId = parseInt(uid);
    }
  },
  methods: {
    isOwner(itemUserId) {
      if (!this.currentUserId || !itemUserId) {
        return false;
      }
      // Handle both string and number comparisons
      return parseInt(itemUserId) === parseInt(this.currentUserId);
    },
    ChatDialog(id) {
      this.uid = id;
      this.chat_dialog = true;
      this.GetQuery();
    },
    SavePost() {
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/yield/",
        data: {
          description: this.description,
          image: this.images,
        },
        headers: {
          "Content-Type": "multipart/form-data",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res.data);
          this.create_post_dialog = false;
          alert("Post create successfully!");
          window.location.reload();
        })
        .catch((error) => {
          this.create_post_dialog = false;
          alert(error.response.data);
          this.errored = true;
          window.location.reload();
        });
    },

    CreatePost() {
      this.create_post_dialog = true;
    },

    Bot() {
      console.log(this.uid);
      axios({
        method: "POST",
        url: "http://127.0.0.1:8000/bot/",
        data: JSON.stringify({
          query: this.query,
          yield_id: this.uid,
        }),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res);
          alert("Thanks for your query!");
          window.location.reload();
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },

    Update(item_id) {
      console.log(item_id);
      axios({
        method: "PUT",
        url: "http://127.0.0.1:8000/yield/",
        data: JSON.stringify({
          food_id: item_id,
        }),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res);
          alert(res.data);
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
          for (let index = 0; index < res.data.length; index++) {
            const element = res.data[index];
            this.items.push(element);
          }

          console.log(this.items);
        })
        .catch((error) => {
          alert(error.response.data);
          this.errored = true;
        });
    },

    GetQuery() {
      axios({
        method: "GET",
        url: "http://127.0.0.1:8000/bot/?id=" + this.uid,
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

    nextPage() {
      if (this.page + 1 <= this.numberOfPages) this.page += 1;
    },
    formerPage() {
      if (this.page - 1 >= 1) this.page -= 1;
    },
    updateItemsPerPage(number) {
      this.itemsPerPage = number;
    },
    
    confirmDelete(yieldId) {
      this.delete_yield_id = yieldId;
      this.delete_dialog = true;
    },
    
    DeleteYield() {
      if (!this.delete_yield_id) {
        return;
      }
      
      axios({
        method: "DELETE",
        url: "http://127.0.0.1:8000/yield/",
        data: JSON.stringify({
          id: this.delete_yield_id,
        }),
        headers: {
          "Content-Type": "application/json; charset=UTF-8",
          Authorization: `token ${this.token}`,
        },
      })
        .then((res) => {
          console.log(res.data);
          this.delete_dialog = false;
          this.delete_yield_id = null;
          alert("Yield deleted successfully!");
          window.location.reload();
        })
        .catch((error) => {
          this.delete_dialog = false;
          this.delete_yield_id = null;
          const errorMessage = error.response?.data || error.message || "Failed to delete yield";
          alert(errorMessage);
          this.errored = true;
        });
    },
  },
};
</script>
